"""Prototype V1.2 — clean halfpipe jump review desktop application.

Run: python app.py
Measurements: hip centre above the blue lip reference line.
Camera changes/zoom require re-calibration. Automatic detection is experimental.
"""
import json
import math
import os
import urllib.request
from pathlib import Path

import cv2
import numpy as np
from PySide6.QtCore import Qt, QTimer, Signal, QThread, QPointF, QRectF, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QFontDatabase, QIcon, QImage, QPainter, QPen, QColor, QPixmap
from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QFileDialog, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QSlider, QStackedWidget, QFrame, QScrollArea,
    QDoubleSpinBox, QSpinBox, QCheckBox, QMessageBox, QProgressBar,
    QSizePolicy, QGraphicsOpacityEffect
)
from measurement import Jump, metres_from_pixels, pixel_height_above_lip, track_candidates

ROOT = Path(__file__).resolve().parent
SAVE_SUFFIX = ".prototype-v1.2.json"
VIDEO_URL = "https://s3.eu-central-1.wasabisys.com/judges/2025_26/freeski/Calgary%20(HP)/FK%20Finals%20-%201%20-%20Camera3%20-%20[10-30-18]%20[12-03-12].mp4"
VIDEO_FILE = ROOT / "video" / "Calgary-Finals-Camera3.mp4"
WHITE = "#ffffff"
INK = "#151b2b"
MUTED = "#87909e"
ACCENT = "#3969ec"
BORDER = "#e8ecf2"

# Inline, scale-independent line icons.
ICONS = {
    "home": '<path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1Z"/><path d="M9 21v-8h6v8"/>',
    "settings": '<path d="M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8Z"/><path d="M19.4 15a1.8 1.8 0 0 0 .3 2l-1.8 1.8a1.8 1.8 0 0 0-2-.3 1.8 1.8 0 0 0-1 1.6V21h-5v-.9a1.8 1.8 0 0 0-1-1.6 1.8 1.8 0 0 0-2 .3L5.1 17a1.8 1.8 0 0 0 .3-2A1.8 1.8 0 0 0 3.8 14H3v-4h.8a1.8 1.8 0 0 0 1.6-1 1.8 1.8 0 0 0-.3-2l1.8-1.8a1.8 1.8 0 0 0 2 .3 1.8 1.8 0 0 0 1-1.6V3h5v.9a1.8 1.8 0 0 0 1 1.6 1.8 1.8 0 0 0 2-.3L19.7 7a1.8 1.8 0 0 0-.3 2 1.8 1.8 0 0 0 1.6 1H22v4h-1a1.8 1.8 0 0 0-1.6 1Z"/>',
    "play": '<path d="m8 5 11 7-11 7Z"/>',
    "pause": '<path d="M8 5v14M16 5v14"/>',
    "prev": '<path d="M6 5v14M18 5 9 12l9 7Z"/>',
    "next": '<path d="M18 5v14M6 5l9 7-9 7Z"/>',
    "open": '<path d="M12 3v12m-4-4 4 4 4-4"/><path d="M4 17v4h16v-4"/>',
    "pin": '<path d="M12 21s7-7 7-12a7 7 0 1 0-14 0c0 5 7 12 7 12Z"/><circle cx="12" cy="9" r="2"/>',
    "delete": '<path d="M4 7h16M10 4h4M6 7l1 14h10l1-14M10 11v6m4-6v6"/>',
    "save": '<path d="M4 3h14l3 3v15H3V3Z"/><path d="M7 3v7h10V3M7 21v-8h10v8"/>',
}

def svg_icon(name, color=INK, size=20):
    from PySide6.QtCore import QByteArray
    from PySide6.QtSvg import QSvgRenderer
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
           f'fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" '
           f'stroke-linejoin="round">{ICONS[name]}</svg>')
    image = QPixmap(size, size)
    image.fill(Qt.GlobalColor.transparent)
    p = QPainter(image)
    QSvgRenderer(QByteArray(svg.encode())).render(p)
    p.end()
    return QIcon(image)

def make_button(text, icon=None, primary=False):
    b = QPushButton(text)
    if icon:
        b.setIcon(svg_icon(icon, "#ffffff" if primary else INK))
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    b.setProperty("primary", primary)
    b.setMinimumHeight(34)
    return b

def textlabel(txt, size=12, color=INK, bold=False):
    w = QLabel(txt)
    w.setStyleSheet(f"color:{color};font-size:{size}px;font-weight:{600 if bold else 400};")
    return w


class VideoCanvas(QWidget):
    clicked_frame = Signal(float, float)

    def __init__(self):
        super().__init__()
        self.frame = None
        self.mode = None
        self.lip_a = self.lip_b = self.hip = None
        self.show_overlay = True
        self.setMinimumSize(360, 215)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCursor(Qt.CursorShape.CrossCursor)

    def frame_rect(self):
        if self.frame is None:
            return QRectF()
        h, w = self.frame.shape[:2]
        factor = min(self.width()/w, self.height()/h)
        sw, sh = w*factor, h*factor
        return QRectF((self.width()-sw)/2, (self.height()-sh)/2, sw, sh)

    def mousePressEvent(self, event):
        if self.frame is None:
            return
        box = self.frame_rect()
        if not box.contains(event.position()):
            return
        ih, iw = self.frame.shape[:2]
        x = (event.position().x()-box.x())/box.width()*iw
        y = (event.position().y()-box.y())/box.height()*ih
        self.clicked_frame.emit(x,y)

    def paintEvent(self, event):
        p=QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor("#101827"))
        if self.frame is None:
            p.setPen(QColor("#aeb6c8"))
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Open a video to get started")
            p.end()
            return
        rgb=cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
        h,w=rgb.shape[:2]
        im=QImage(rgb.data,w,h,rgb.strides[0],QImage.Format.Format_RGB888).copy()
        box=self.frame_rect()
        p.drawImage(box,im)
        def map_point(pt):
            return QPointF(box.x()+pt[0]/w*box.width(),box.y()+pt[1]/h*box.height())
        if self.show_overlay:
            if self.lip_a and self.lip_b:
                p.setPen(QPen(QColor("#4cbaff"),3))
                p.drawLine(map_point(self.lip_a),map_point(self.lip_b))
            for v,color in ((self.lip_a,"#4cbaff"),(self.lip_b,"#4cbaff"),(self.hip,"#fb963b")):
                if v:
                    p.setPen(QPen(QColor("white"),2))
                    p.setBrush(QColor(color))
                    p.drawEllipse(map_point(v),6,6)
            if self.hip and self.lip_a and self.lip_b:
                from measurement import lip_y_at_x
                target=(self.hip[0],lip_y_at_x(self.lip_a,self.lip_b,self.hip[0]))
                p.setPen(QPen(QColor("#ffd54d"),2,Qt.PenStyle.DashLine))
                p.drawLine(map_point(self.hip),map_point(target))
        p.end()


class JumpTimeline(QWidget):
    seek = Signal(int)
    def __init__(self):
        super().__init__()
        self.total=1
        self.current=0
        self.jumps=[]
        self.setMinimumHeight(47)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def paintEvent(self, event):
        p=QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        left,right=16,self.width()-16
        p.setPen(QPen(QColor("#e5eaf2"),7,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
        p.drawLine(left,23,right,23)
        pos=lambda frame:left+(right-left)*frame/max(1,self.total-1)
        p.setPen(QPen(QColor(ACCENT),7,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
        p.drawLine(left,23,int(pos(self.current)),23)
        for j in self.jumps:
            p.setBrush(QColor("#f59e0b" if j.source=="auto candidate" else "#15b89a"))
            p.setPen(QPen(QColor("white"),2))
            p.drawEllipse(QPointF(pos(j.frame),23),6,6)
        p.setBrush(QColor(ACCENT))
        p.setPen(QPen(QColor("white"),2))
        p.drawEllipse(QPointF(pos(self.current),23),8,8)
        p.end()

    def mousePressEvent(self,event):
        x=max(0,min(self.width()-32,event.position().x()-16))
        clicked_frame=round(x/max(1,self.width()-32)*(self.total-1))
        # Prefer an actual jump marker when clicking close to a visible dot.
        threshold=max(1,round(self.total*10/max(1,self.width()-32)))
        nearby=[j for j in self.jumps if abs(j.frame-clicked_frame)<=threshold]
        self.seek.emit(min(nearby,key=lambda j:abs(j.frame-clicked_frame)).frame if nearby else clicked_frame)


class Worker(QThread):
    finished_jumps = Signal(object)
    failed = Signal(str)
    progress = Signal(int)

    def __init__(self, path, scale, stride, sensitivity):
        super().__init__()
        self.args = (path, scale, stride, sensitivity)

    def run(self):
        try:
            from automatic import analyze_video
            self.finished_jumps.emit(analyze_video(*self.args, progress=self.progress.emit))
        except Exception as exc:
            self.failed.emit(str(exc))


class DefaultVideoDownload(QThread):
    progress = Signal(int)
    complete = Signal(str)
    failed = Signal(str)

    def run(self):
        try:
            VIDEO_FILE.parent.mkdir(parents=True, exist_ok=True)
            temp = VIDEO_FILE.with_suffix(".part")
            request = urllib.request.Request(VIDEO_URL, headers={"User-Agent": "PrototypeV1.2"})
            with urllib.request.urlopen(request, timeout=45) as response, open(temp, "wb") as dest:
                total = int(response.headers.get("Content-Length") or 0)
                written = 0
                while True:
                    chunk = response.read(1024*1024)
                    if not chunk:
                        break
                    dest.write(chunk)
                    written += len(chunk)
                    if total:
                        self.progress.emit(min(99, int(written*100/total)))
            temp.replace(VIDEO_FILE)
            self.complete.emit(str(VIDEO_FILE))
        except Exception as exc:
            self.failed.emit(str(exc))


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prototype V1.3 — Halfpipe")
        self.setFixedSize(960, 610)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
        self.cap=None
        self.path=None
        self.fps=30.
        self.frames=1
        self.frame_index=0
        self.jumps=[]
        self.mode=""
        self.lip_a=self.lip_b=self.hip=None
        self.pixels_per_metre=0.
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.next_frame)
        self.build_ui()
        self.update_display()
        QTimer.singleShot(200, self.load_default_video)

    def build_ui(self):
        root=QWidget()
        self.setCentralWidget(root)
        layout=QHBoxLayout(root)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        sidebar=QFrame()
        sidebar.setObjectName("side")
        sidebar.setFixedWidth(142)
        sl=QVBoxLayout(sidebar)
        sl.setContentsMargins(12,23,12,15)
        sl.setSpacing(7)
        logo=QLabel("◢  Prototype V1.3")
        logo.setStyleSheet("font-weight:700;font-size:15px;margin-bottom:16px;")
        sl.addWidget(logo)
        self.home_btn=make_button("  Home","home")
        self.settings_btn=make_button("  Settings","settings")
        sl.addWidget(self.home_btn)
        sl.addWidget(self.settings_btn)
        sl.addStretch()
        sl.addWidget(textlabel("Automatic analysis • Beta",10,MUTED))
        layout.addWidget(sidebar)
        self.pages=QStackedWidget()
        layout.addWidget(self.pages,1)
        self.build_home()
        self.build_settings()
        self.home_btn.clicked.connect(lambda:self.show_page(0))
        self.settings_btn.clicked.connect(lambda:self.show_page(1))
        self.show_page(0)

    def build_home(self):
        page=QWidget()
        main=QVBoxLayout(page)
        main.setContentsMargins(22,18,22,16)
        main.setSpacing(9)
        top=QHBoxLayout()
        title=textlabel("Jump analysis",21,INK,True)
        top.addWidget(title)
        top.addStretch()
        self.open_btn=make_button("Open video","open",True)
        self.open_btn.clicked.connect(self.open_video)
        top.addWidget(self.open_btn)
        main.addLayout(top)
        main.addWidget(textlabel("Automatic jump detection and frame-by-frame review",12,MUTED))
        self.canvas=VideoCanvas()
        self.canvas.clicked_frame.connect(self.canvas_clicked)
        main.addWidget(self.canvas,1)
        playback=QHBoxLayout()
        self.prev_btn=make_button("","prev")
        self.play_btn=make_button("","play")
        self.next_btn=make_button("","next")
        for b in [self.prev_btn,self.play_btn,self.next_btn]:
            b.setFixedWidth(48)
            playback.addWidget(b)
        self.prev_btn.clicked.connect(self.previous_frame)
        self.play_btn.clicked.connect(self.toggle_play)
        self.next_btn.clicked.connect(self.next_frame)
        self.counter=textlabel("Frame 0 / 0",12,MUTED)
        playback.addSpacing(15)
        playback.addWidget(self.counter)
        playback.addStretch()
        self.measure=textlabel("— m",20,INK,True)
        playback.addWidget(self.measure)
        main.addLayout(playback)
        self.timeline=JumpTimeline()
        self.timeline.seek.connect(self.seek)
        main.addWidget(self.timeline)
        description=QHBoxLayout()
        description.addWidget(textlabel("Orange dots: detected candidates • estimates require calibration",11,MUTED))
        description.addStretch()
        main.addLayout(description)
        actions=QHBoxLayout()
        self.lip_btn=make_button("Set lip line","pin")
        self.hip_btn=make_button("Select hip","pin")
        self.add_btn=make_button("Save jump","save",True)
        self.remove_btn=make_button("Remove marker","delete")
        self.scan_btn=make_button("Auto-detect jumps",primary=True)
        for btn in [self.scan_btn,self.remove_btn]:
            actions.addWidget(btn)
        actions.addStretch()
        main.addLayout(actions)
        self.notice=textlabel("Select two points along the blue lip line, then the athlete's hip.",11,MUTED)
        main.addWidget(self.notice)
        self.lip_btn.clicked.connect(lambda:self.set_mode("lip"))
        self.hip_btn.clicked.connect(lambda:self.set_mode("hip"))
        self.add_btn.clicked.connect(self.add_jump)
        self.remove_btn.clicked.connect(self.remove_jump)
        self.scan_btn.clicked.connect(self.scan)
        self.pages.addWidget(page)

    def build_settings(self):
        scroller=QScrollArea()
        scroller.setWidgetResizable(True)
        scroller.setFrameShape(QFrame.Shape.NoFrame)
        page=QWidget()
        outer=QVBoxLayout(page)
        outer.setContentsMargins(30,24,30,24)
        outer.setSpacing(12)
        outer.addWidget(textlabel("Settings",22,INK,True))
        outer.addWidget(textlabel("Measurement & detection preferences",12,MUTED))
        outer.addSpacing(7)
        outer.addWidget(textlabel("MEASUREMENT",11,MUTED,True))
        outer.addWidget(textlabel("Pixels per metre",13,INK,True))
        outer.addWidget(textlabel("Set a real-world scale for this camera framing. 0 = unknown.",11,MUTED))
        self.scale=QDoubleSpinBox()
        self.scale.setRange(0,100000)
        self.scale.setDecimals(3)
        self.scale.setSingleStep(1)
        self.scale.setSuffix(" px / m")
        self.scale.setValue(0)
        self.scale.valueChanged.connect(self.scale_changed)
        self.scale.setMaximumWidth(400)
        outer.addWidget(self.scale)
        outer.addWidget(textlabel("Use a known-length object/segment in the same depth plane as the athlete. Recalibrate after zoom.",11,MUTED))
        outer.addSpacing(14)
        outer.addWidget(textlabel("DETECTION",11,MUTED,True))
        outer.addWidget(textlabel("Analyze every Nth frame",13,INK,True))
        self.duration=QSpinBox()
        self.duration.setRange(1,30)
        self.duration.setValue(4)
        self.duration.setSuffix(" frames")
        self.duration.setMaximumWidth(400)
        outer.addWidget(self.duration)
        outer.addWidget(textlabel("Candidate sensitivity",13,INK,True))
        self.sensitivity=QSlider(Qt.Orientation.Horizontal)
        self.sensitivity.setRange(1,100)
        self.sensitivity.setValue(45)
        self.sensitivity.setMaximumWidth(400)
        outer.addWidget(self.sensitivity)
        outer.addWidget(textlabel("Pose detection finds the hip without clicking. Blue-lip and jump results are estimates.",11,MUTED))
        outer.addSpacing(14)
        outer.addWidget(textlabel("VIEW",11,MUTED,True))
        self.overlay=QCheckBox("Show lip / hip markers")
        self.overlay.setChecked(True)
        self.overlay.toggled.connect(self.overlay_changed)
        outer.addWidget(self.overlay)
        self.autosave=QCheckBox("Save measurements beside video")
        self.autosave.setChecked(True)
        outer.addWidget(self.autosave)
        outer.addSpacing(20)
        outer.addWidget(textlabel("Made by Oliver Weiner, 2EHIF",10,"#a6aeba"))
        outer.addStretch()
        scroller.setWidget(page)
        scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.pages.addWidget(scroller)

    def show_page(self,index):
        if self.pages.currentIndex() != index:
            widget = self.pages.widget(index)
            self.pages.setCurrentIndex(index)
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
            animation = QPropertyAnimation(effect, b"opacity", self)
            animation.setDuration(190)
            animation.setStartValue(0.72)
            animation.setEndValue(1.0)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            animation.start()
            self._page_animation = animation
        self.home_btn.setProperty("selected",index==0)
        self.settings_btn.setProperty("selected",index==1)
        for b in (self.home_btn,self.settings_btn):
            b.style().unpolish(b)
            b.style().polish(b)

    def set_mode(self,mode):
        if not self.cap:
            self.notice.setText("Open a video first.")
            return
        self.mode=mode
        if mode=="lip":
            self.lip_a=self.lip_b=None
            self.notice.setText("Click the first and second points on the blue lip line.")
        else:
            self.notice.setText("Click the athlete's HIP centre on this frame.")
        self.update_display()

    def canvas_clicked(self,x,y):
        if self.mode=="lip":
            if self.lip_a is None:
                self.lip_a=[x,y]
                self.notice.setText("Now click a second point along the same lip.")
            else:
                self.lip_b=[x,y]
                self.mode=""
                self.notice.setText("Lip line selected. Select hip for the current frame.")
        elif self.mode=="hip":
            self.hip=[x,y]
            self.mode=""
            self.notice.setText("Hip selected. Save jump to add a marker.")
        self.update_display()

    def load_default_video(self):
        if VIDEO_FILE.exists() and VIDEO_FILE.stat().st_size > 1024 * 1024:
            self.load_video(str(VIDEO_FILE))
            self.notice.setText("Calgary video loaded. Click Auto-detect jumps.")
            return
        self.notice.setText("Downloading the Calgary video…")
        self.open_btn.setEnabled(False)
        self.downloader = DefaultVideoDownload()
        self.downloader.progress.connect(
            lambda p: self.notice.setText(f"Downloading Calgary video… {p}%"))
        self.downloader.complete.connect(self.default_video_ready)
        self.downloader.failed.connect(self.default_video_failed)
        self.downloader.start()

    def default_video_ready(self, path):
        self.open_btn.setEnabled(True)
        self.load_video(path)
        self.notice.setText("Calgary video ready. Click Auto-detect jumps.")

    def default_video_failed(self, error):
        self.open_btn.setEnabled(True)
        self.notice.setText("Download unavailable; use Open video to choose a local MP4. " + error[:75])

    def open_video(self):
        filename,_=QFileDialog.getOpenFileName(self,"Open halfpipe footage","","Video files (*.mp4 *.mov *.avi *.mkv);;All files (*)")
        if filename:
            self.load_video(filename)

    def load_video(self,filename):
        self.timer.stop()
        if self.cap:
            self.cap.release()
        self.cap=cv2.VideoCapture(filename)
        if not self.cap.isOpened():
            self.cap=None
            QMessageBox.warning(self,"Video error","Cannot read this video. Check the file and codec.")
            return
        self.path=filename
        self.fps=self.cap.get(cv2.CAP_PROP_FPS) or 30
        self.frames=max(1,int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)))
        self.frame_index=0
        self.jumps=[]
        self.lip_a=self.lip_b=self.hip=None
        self.pixels_per_metre=0
        self.scale.blockSignals(True)
        self.scale.setValue(0)
        self.scale.blockSignals(False)
        self.read_sidecar()
        self.timeline.total=self.frames
        self.seek(0)
        self.setWindowTitle(f"Prototype V1.3 — {Path(filename).name}")
        QTimer.singleShot(800, self.scan)  # auto-analyze whenever a new video loads

    def seek(self,n):
        if not self.cap:
            return
        self.frame_index=max(0,min(self.frames-1,int(n)))
        self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.frame_index)
        ok,img=self.cap.read()
        if not ok:
            self.notice.setText("Unable to read requested frame.")
            return
        self.canvas.frame=img
        self.update_display()

    def update_display(self):
        self.canvas.lip_a=self.lip_a
        self.canvas.lip_b=self.lip_b
        self.canvas.hip=self.hip
        self.canvas.update()
        self.timeline.current=self.frame_index
        self.timeline.jumps=self.jumps
        self.timeline.update()
        self.counter.setText(f"Frame {self.frame_index+1:,} / {self.frames:,}     {self.frame_index/self.fps:,.2f}s")
        current=next((j for j in self.jumps if j.frame==self.frame_index),None)
        if current:
            if current.height_m is not None:
                self.measure.setText(f"{current.height_m:.2f} m  ·  estimated")
            elif current.pixel_height is not None:
                self.measure.setText(f"{current.pixel_height:.0f} px  ·  uncalibrated")
            else:
                self.measure.setText("Candidate  ·  unmeasured")
        else:
            px=pixel_height_above_lip(self.hip,self.lip_a,self.lip_b)
            if px is None:
                self.measure.setText("— m")
            else:
                metres=metres_from_pixels(px,self.pixels_per_metre)
                self.measure.setText(f"{metres:.2f} m · estimated" if metres is not None else f"{px:.0f} px · uncalibrated")

    def previous_frame(self):
        self.timer.stop()
        self.play_btn.setIcon(svg_icon("play"))
        self.seek(self.frame_index-1)

    def next_frame(self):
        if self.frame_index>=self.frames-1:
            self.timer.stop()
            self.play_btn.setIcon(svg_icon("play"))
        else:
            self.seek(self.frame_index+1)

    def toggle_play(self):
        if not self.cap:
            return
        if self.timer.isActive():
            self.timer.stop()
            self.play_btn.setIcon(svg_icon("play"))
        else:
            self.timer.start(max(1,round(1000/self.fps)))
            self.play_btn.setIcon(svg_icon("pause"))

    def add_jump(self):
        if not self.cap:
            return
        if self.hip is None or self.lip_a is None or self.lip_b is None:
            self.notice.setText("Set the blue lip line and hip before saving a measured jump.")
            return
        px=pixel_height_above_lip(self.hip,self.lip_a,self.lip_b)
        metres=metres_from_pixels(px,self.pixels_per_metre)
        j=Jump(self.frame_index,metres,px,"manual")
        self.jumps=[other for other in self.jumps if other.frame!=j.frame]+[j]
        self.jumps.sort(key=lambda x:x.frame)
        self.notice.setText("Jump saved. Metre values are estimates until calibration is validated.")
        self.save_sidecar()
        self.update_display()

    def remove_jump(self):
        self.jumps=[j for j in self.jumps if j.frame!=self.frame_index]
        self.save_sidecar()
        self.update_display()

    def scan(self):
        if not self.cap:
            self.notice.setText("Wait for the video or open your local MP4 first.")
            return
        self.timer.stop()
        self.scan_btn.setEnabled(False)
        self.notice.setText("Preparing pose AI. First run may download the model…")
        self.worker=Worker(self.path,self.pixels_per_metre,self.duration.value(),self.sensitivity.value()/100)
        self.worker.progress.connect(lambda p: self.notice.setText(f"Analyzing video… {p}%"))
        self.worker.finished_jumps.connect(self.scan_done)
        self.worker.failed.connect(self.scan_failed)
        self.worker.start()

    def scan_done(self,proposals):
        existing={j.frame for j in self.jumps}
        self.jumps.extend(j for j in proposals if j.frame not in existing)
        self.jumps.sort(key=lambda x:x.frame)
        self.notice.setText(f"Found {len(proposals)} automatic candidates. Review orange markers; metres need calibration.")
        self.scan_btn.setEnabled(True)
        self.update_display()
        self.save_sidecar()

    def scan_failed(self,error):
        self.scan_btn.setEnabled(True)
        QMessageBox.warning(self,"Tracking failed",error)
        self.notice.setText("Automatic analysis failed. Check the model installation or video.")

    def scale_changed(self,value):
        self.pixels_per_metre=value
        for jump in self.jumps:
            if jump.pixel_height is not None:
                jump.height_m=metres_from_pixels(jump.pixel_height,value)
        self.save_sidecar()
        self.update_display()

    def overlay_changed(self,enabled):
        self.canvas.show_overlay=enabled
        self.canvas.update()

    def save_sidecar(self):
        if not self.path or not self.autosave.isChecked():
            return
        data={
            "version":"1.2","video":Path(self.path).name,
            "pixels_per_metre":self.pixels_per_metre,
            "lip_a":self.lip_a,"lip_b":self.lip_b,
            "jumps":[j.to_dict() for j in self.jumps],
            "warning":"Values are approximate: perspective, zoom, camera motion and hip tracking affect accuracy."
        }
        try:
            Path(self.path+SAVE_SUFFIX).write_text(json.dumps(data,indent=2),encoding="utf-8")
        except OSError as exc:
            self.notice.setText(f"Cannot save sidecar: {exc}")

    def read_sidecar(self):
        sidecar=Path(self.path+SAVE_SUFFIX)
        if not sidecar.exists():
            return
        try:
            data=json.loads(sidecar.read_text(encoding="utf-8"))
            self.lip_a=data.get("lip_a")
            self.lip_b=data.get("lip_b")
            self.pixels_per_metre=float(data.get("pixels_per_metre") or 0)
            self.scale.blockSignals(True)
            self.scale.setValue(self.pixels_per_metre)
            self.scale.blockSignals(False)
            self.jumps=[Jump(**j) for j in data.get("jumps",[])
                        if 0<=int(j["frame"])<self.frames]
        except (OSError,ValueError,KeyError,TypeError) as exc:
            self.notice.setText(f"Measurements could not be restored: {exc}")

    def closeEvent(self,event):
        self.timer.stop()
        if self.cap:
            self.cap.release()
        super().closeEvent(event)


def main():
    app=QApplication([])
    app.setStyle("Fusion")
    font_file=ROOT/"assets"/"Inter-Regular.ttf"
    if font_file.exists():
        QFontDatabase.addApplicationFont(str(font_file))
    app.setFont(QFont("Inter" if "Inter" in QFontDatabase.families() else "Segoe UI", 10))
    app.setStyleSheet("""
        QWidget { background:#ffffff; color:#151b2b; font-family:Inter,'Segoe UI',sans-serif; font-size:12px; }
        QFrame#side { background:#fbfcff; border-right:1px solid #e8ecf2; }
        QFrame#side QLabel { background:transparent; }
        QPushButton { background:#f6f8fb; border:1px solid #e6ebf1; border-radius:9px; padding:7px 10px; text-align:center; }
        QPushButton:hover { background:#eaf0ff; }
        QPushButton:disabled { color:#afb7c7; }
        QPushButton[primary="true"] { background:#3969ec; border-color:#3969ec; color:white; font-weight:600; }
        QPushButton[primary="true"]:hover { background:#2859d8; }
        QPushButton[selected="true"] { background:#eaf0ff; color:#2254cf; font-weight:600; }
        QDoubleSpinBox,QSpinBox { border:1px solid #e2e8f0; border-radius:10px; min-height:39px; padding-left:17px; padding-right:12px; }
        QScrollArea { border:0; }
        QSlider::groove:horizontal { height:5px; background:#e3e9f2; border-radius:2px; }
        QSlider::handle:horizontal { width:17px; margin:-6px 0; background:#3969ec; border-radius:8px; }
        QCheckBox { spacing:9px; }
    """)
    win=App()
    icon=ROOT/"assets"/"app-icon.svg"
    if icon.exists():
        win.setWindowIcon(QIcon(str(icon)))
    win.show()
    app.exec()

if __name__=="__main__":
    main()
