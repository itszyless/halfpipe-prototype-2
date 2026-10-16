"""Prototype V1.2 — clean halfpipe jump review desktop application.

Run: python app.py
Measurements: hip centre above the blue lip reference line.
Camera changes/zoom require re-calibration. Automatic detection is experimental.
"""
import json
import base64
import math
import os
import urllib.request
from pathlib import Path

import cv2
import numpy as np
from PySide6.QtCore import Qt, QTimer, Signal, QThread, QPointF, QRectF, QSize, QPropertyAnimation, QEasingCurve
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
VIDEO_FILE = ROOT / "video" / "prototypev1.mp4"
WHITE = "#0c0e12"
INK = "#f3f5f8"
MUTED = "#9aa2b1"
ACCENT = "#c4cce0"
BORDER = "#282d36"

# Inline, scale-independent line icons.
ICONS = {
    "home": '<path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1Z"/><path d="M9 21v-8h6v8"/>',
    "settings": '<path d="M12 2.5 14 3l1 2.2 2.2.9 2.2-.8 2.4 2.4-.8 2.2.9 2.2 2.2 1v3.4l-2.2 1-1 2.2.8 2.2-2.4 2.4-2.2-.8-2.2.9-1 2.2h-3.4l-1-2.2-2.2-.9-2.2.8-2.4-2.4.8-2.2-.9-2.2-2.2-1v-3.4l2.2-1 .9-2.2-.8-2.2 2.4-2.4 2.2.8 2.2-.9 1-2.2Z" transform="translate(2.1 2.1) scale(.82)"/><circle cx="12" cy="12" r="3.4"/>',
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

def image_icon(asset_name):
    # These raster assets come from the uploaded artwork, not generated SVGs.
    path = ROOT / "assets" / (asset_name + ".png.b64")
    pixmap = QPixmap()
    if path.exists():
        pixmap.loadFromData(base64.b64decode(path.read_text(encoding="ascii").strip()), "PNG")
    return QIcon(pixmap)


def make_button(text, icon=None, primary=False):
    b = QPushButton(text)
    if icon:
        b.setIcon(image_icon("settings-icon") if icon == "settings" else image_icon("home-icon") if icon == "home" else svg_icon(icon, "#ffffff" if primary else INK))
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    b.setProperty("primary", primary)
    b.setMinimumHeight(34)
    return b

def textlabel(txt, size=12, color=INK, bold=False):
    w = QLabel(txt)
    w.setStyleSheet(f"color:{color};font-size:{size}px;font-weight:{600 if bold else 400};")
    w.setWordWrap(True)
    return w


class VideoCanvas(QWidget):
    clicked_frame = Signal(float, float)

    def __init__(self):
        super().__init__()
        self.frame = None
        self.mode = None
        self.lip_a = self.lip_b = self.hip = None
        self.show_overlay = True
        self.pose = None
        self.fixed_baseline = None
        self.pixels_per_metre = 0
        self.zoom=1.0
        self.pan_x=.5
        self.pan_y=.5
        self._drag_start=None
        self._left_pending=False
        self._dragging=False
        self.pan_mode=False
        self.setMinimumSize(360, 180)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCursor(Qt.CursorShape.CrossCursor)

    def frame_rect(self):
        if self.frame is None:
            return QRectF()
        h, w = self.frame.shape[:2]
        factor = min(self.width()/w, self.height()/h)*self.zoom
        sw, sh = w*factor, h*factor
        return QRectF(self.width()/2-self.pan_x*sw,self.height()/2-self.pan_y*sh,sw,sh)

    def mousePressEvent(self, event):
        if self.frame is None:
            return
        self._press_pos = event.position()
        if event.button() == Qt.MouseButton.RightButton or self.pan_mode:
            self._drag_start = event.position()
            self._dragging = True
            event.accept()
            return
        if event.button() != Qt.MouseButton.LeftButton:
            event.ignore()
            return
        # Only release of a genuine left click can select a calibration mark.
        self._left_pending = True
        event.accept()

    def wheelEvent(self,event):
        if self.frame is None:
            return
        old=self.frame_rect()
        mouse=event.position()
        fx=(mouse.x()-old.x())/old.width()
        fy=(mouse.y()-old.y())/old.height()
        self.zoom=max(1.,min(12.,self.zoom*(1.25 if event.angleDelta().y()>0 else .8)))
        h,w=self.frame.shape[:2]
        scale=min(self.width()/w,self.height()/h)*self.zoom
        self.pan_x=max(0.,min(1.,fx-(mouse.x()-self.width()/2)/(w*scale)))
        self.pan_y=max(0.,min(1.,fy-(mouse.y()-self.height()/2)/(h*scale)))
        self.update()

    def mouseMoveEvent(self,event):
        if self._drag_start is not None and self.frame is not None:
            dx=event.position().x()-self._drag_start.x()
            dy=event.position().y()-self._drag_start.y()
            area=self.frame_rect()
            self.pan_x=max(0.,min(1.,self.pan_x-dx/area.width()))
            self.pan_y=max(0.,min(1.,self.pan_y-dy/area.height()))
            self._drag_start=event.position()
            self.update()
            event.accept()
        elif getattr(self,"_left_pending",False):
            if (event.position()-self._press_pos).manhattanLength()>7:
                self._left_pending=False

    def mouseReleaseEvent(self,event):
        if self._drag_start is not None:
            self._drag_start=None
            self._dragging=False
            event.accept()
            return
        if event.button()!=Qt.MouseButton.LeftButton or not self._left_pending:
            return
        self._left_pending=False
        if self.pan_mode or self.frame is None:
            return
        box=self.frame_rect()
        if not box.contains(event.position()):
            return
        ih,iw=self.frame.shape[:2]
        px=(event.position().x()-box.x())/box.width()*iw
        py=(event.position().y()-box.y())/box.height()*ih
        if 0<=px<iw and 0<=py<ih:
            self.clicked_frame.emit(px,py)
        event.accept()

    def contextMenuEvent(self,event):
        # Suppress native right-click menu while calibrating or panning.
        event.accept()

    def reset_zoom(self):
        self.zoom=1.
        self.pan_x=.5
        self.pan_y=.5
        self.update()

    def paintEvent(self, event):
        p=QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor("#080a0e"))
        if self.frame is None:
            p.setPen(QColor("#aeb6c8"))
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Waiting for video")
            p.end()
            return
        h,w=self.frame.shape[:2]
        factor=min(1.,max(600,int(max(self.width(),self.height())*1.5))/max(w,h)) if self.zoom<=1.05 else 1.
        display=self.frame if factor>=1. else cv2.resize(self.frame,(max(1,round(w*factor)),max(1,round(h*factor))))
        rgb=cv2.cvtColor(display,cv2.COLOR_BGR2RGB)
        dh,dw=rgb.shape[:2]
        im=QImage(rgb.data,dw,dh,rgb.strides[0],QImage.Format.Format_RGB888).copy()
        box=self.frame_rect()
        p.setClipRect(self.rect())
        p.drawImage(box,im)
        def map_point(pt):
            return QPointF(box.x()+pt[0]/w*box.width(),box.y()+pt[1]/h*box.height())
        if self.show_overlay:
            if self.fixed_baseline is not None:
                p.setPen(QPen(QColor("#48afff"),2))
                p.drawLine(map_point((0,self.fixed_baseline)),map_point((w,self.fixed_baseline)))
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
            if self.pose:
                from automatic import SKELETON
                pts=self.pose["points"]
                conf=self.pose["conf"]
                p.setPen(QPen(QColor("#9af5c8"), 2))
                for a,b in SKELETON:
                    if conf[a]>(.55 if a in (15,16) else .30) and conf[b]>(.55 if b in (15,16) else .30):
                        p.drawLine(map_point(pts[a]),map_point(pts[b]))
                for i,pt in enumerate(pts):
                    if conf[i]>(.55 if i in (15,16) else .30):
                        p.setBrush(QColor("#9af5c8"))
                        p.drawEllipse(map_point(pt),3,3)
                baseline=self.pose.get("baseline_y")
                foot=self.pose.get("foot_y")
                standing=self.pose.get("standing_y")
                x=self.pose.get("foot_x",w/2)
                ruler_x=w*.91
                if baseline is not None:
                    p.setPen(QPen(QColor("#48afff"),2))
                    p.drawLine(map_point((0,baseline)),map_point((w,baseline)))
                if foot is not None and standing is not None:
                    p.setPen(QPen(QColor("#ffc788"),2,Qt.PenStyle.DashLine))
                    p.drawLine(map_point((x,foot)),map_point((x,standing)))
                    p.setPen(QPen(QColor("#f7d097"),1,Qt.PenStyle.DashLine))
                    p.drawLine(map_point((x,foot)),map_point((ruler_x,foot)))
                    p.setBrush(QColor("#ffd19a"))
                    p.drawEllipse(map_point((x,foot)),5,5)
                    height=max(0.,standing-foot)
                    if self.pixels_per_metre>0:
                        label=f"{height/self.pixels_per_metre:.2f} m approx."
                    else:
                        label=f"{height:.0f} px | calibrate ruler"
                    p.setPen(QColor("#f1f5fd"))
                    pos=map_point((ruler_x,foot))
                    p.drawText(QPointF(max(4.,pos.x()-165),max(16.,pos.y()-12)),label)
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
        p.setPen(QPen(QColor("#303541"),7,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
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

    def __init__(self, path, scale, stride, sensitivity, force=False):
        super().__init__()
        self.args = (path, scale, stride, sensitivity)
        self.force=force

    def run(self):
        try:
            from automatic import analyze_video
            self.finished_jumps.emit(analyze_video(*self.args, progress=self.progress.emit,force=self.force))
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
        self.setFixedSize(1050, 680)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
        self.cap=None
        self.path=None
        self.fps=30.
        self.frames=1
        self.frame_index=0
        self._next_decode_index=0
        self.jumps=[]
        self.tracks={}
        self.mode=""
        self.lip_a=self.lip_b=self.hip=None
        self.pixels_per_metre=0.
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.next_frame)
        self.build_ui()
        self.update_display()
        QTimer.singleShot(200, self.load_default_video)

    def build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        shell = QHBoxLayout(root)
        shell.setContentsMargins(0, 0, 0, 0)
        shell.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("side")
        sidebar.setFixedWidth(84)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(14, 23, 14, 18)
        side.setSpacing(4)

        brand = QLabel("")
        brand.setObjectName("brand")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        side.addWidget(brand)
        version = QLabel("V1.3")
        version.setObjectName("version")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        side.addWidget(version)
        side.addSpacing(38)

        self.home_btn = make_button("", "home")
        self.home_btn.setIconSize(QSize(32, 32))
        self.settings_btn = make_button("", "settings")
        for button in (self.home_btn, self.settings_btn):
            button.setObjectName("navButton")
            button.setFixedSize(54, 54)
            button.setIconSize(QSize(32, 32))
            side.addWidget(button, alignment=Qt.AlignmentFlag.AlignHCenter)
        side.addStretch()
        
        shell.addWidget(sidebar)

        self.pages = QStackedWidget()
        shell.addWidget(self.pages, 1)
        self.build_home()
        self.build_settings()
        self.home_btn.setToolTip("Home")
        self.settings_btn.setToolTip("Settings")
        self.home_btn.clicked.connect(lambda: self.show_page(0))
        self.settings_btn.clicked.connect(lambda: self.show_page(1))
        self.show_page(0)

    def build_home(self):
        page = QWidget()
        main = QVBoxLayout(page)
        main.setContentsMargins(27, 25, 27, 20)
        main.setSpacing(0)

        top = QHBoxLayout()
        heading = QVBoxLayout()
        heading.setSpacing(4)
        heading.addWidget(textlabel("Video analysis", 23, INK, True))
        heading.addWidget(textlabel("Prototype V1  /  Jump height experiment", 11, MUTED))
        top.addLayout(heading)
        top.addStretch()
        self.open_btn = make_button("Change video", "open")
        self.open_btn.clicked.connect(self.open_video)
        top.addWidget(self.open_btn, alignment=Qt.AlignmentFlag.AlignVCenter)
        main.addLayout(top)
        main.addSpacing(18)

        self.canvas = VideoCanvas()
        self.canvas.clicked_frame.connect(self.canvas_clicked)
        self.canvas.setObjectName("video")
        main.addWidget(self.canvas, 1)
        main.addSpacing(13)

        transport = QHBoxLayout()
        transport.setSpacing(7)
        self.prev_btn = make_button("", "prev")
        self.play_btn = make_button("", "play")
        self.next_btn = make_button("", "next")
        for button in (self.prev_btn, self.play_btn, self.next_btn):
            button.setObjectName("transport")
            button.setFixedSize(37, 34)
            transport.addWidget(button)
        self.prev_btn.clicked.connect(self.previous_frame)
        self.play_btn.clicked.connect(self.toggle_play)
        self.next_btn.clicked.connect(self.next_frame)
        transport.addSpacing(8)
        self.counter = textlabel("Frame 0 / 0", 11, MUTED)
        transport.addWidget(self.counter)
        transport.addStretch()
        self.measure = textlabel("—", 21, INK, True)
        transport.addWidget(self.measure)
        main.addLayout(transport)
        main.addSpacing(10)

        self.timeline = JumpTimeline()
        self.timeline.seek.connect(self.seek)
        self.timeline.setFixedHeight(36)
        main.addWidget(self.timeline)
        main.addSpacing(8)

        tools = QHBoxLayout()
        tools.setSpacing(8)
        self.calibrate_btn = make_button("Calibrate ruler")
        self.pan_btn=make_button("Pan: off")
        self.pan_btn.setCheckable(True)
        self.pan_btn.toggled.connect(self.set_pan_mode)
        self.reset_zoom_btn=make_button("Reset zoom")
        self.reset_zoom_btn.clicked.connect(self.canvas.reset_zoom)
        self.calibrate_btn.clicked.connect(self.begin_ruler_calibration)
        self.scan_btn = make_button("Run detection", primary=True)
        self.remove_btn = make_button("Remove point")
        self.scan_btn.clicked.connect(self.scan)
        self.rescan_btn=make_button("Reanalyze")
        self.rescan_btn.clicked.connect(lambda: self.scan(force=True))
        self.remove_btn.clicked.connect(self.remove_jump)
        tools.addWidget(self.scan_btn)
        tools.addWidget(self.rescan_btn)
        tools.addWidget(self.calibrate_btn)
        tools.addWidget(self.reset_zoom_btn)
        tools.addWidget(self.pan_btn)
        tools.addWidget(self.remove_btn)
        tools.addStretch()
        tools.addWidget(textlabel("●  Detected jump", 10, MUTED))
        main.addLayout(tools)
        main.addSpacing(11)

        self.notice = textlabel("Preparing video…", 11, MUTED)
        self.notice.setObjectName("status")
        main.addWidget(self.notice)

        # Legacy manual helpers remain available internally for troubleshooting,
        # but are intentionally absent from the streamlined primary interface.
        self.lip_btn = make_button("Set lip line", "pin")
        self.hip_btn = make_button("Select hip", "pin")
        self.add_btn = make_button("Save jump", "save")
        self.lip_btn.clicked.connect(lambda: self.set_mode("lip"))
        self.hip_btn.clicked.connect(lambda: self.set_mode("hip"))
        self.add_btn.clicked.connect(self.add_jump)
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
        outer.addWidget(textlabel("Known ruler distance",13,INK,True))
        self.reference_m=QDoubleSpinBox()
        self.reference_m.setRange(.01,10)
        self.reference_m.setDecimals(2)
        self.reference_m.setValue(0.50)
        self.reference_m.setSuffix(" m")
        self.reference_m.setMaximumWidth(460)
        self.reference_m.lineEdit().setTextMargins(20,0,8,0)
        outer.addWidget(self.reference_m)
        outer.addWidget(textlabel("Distance between two readable ruler marks.",11,MUTED))
        outer.addWidget(textlabel("Calculated pixels per metre",13,INK,True))
        outer.addWidget(textlabel("Set a real-world scale for this camera framing. 0 = unknown.",11,MUTED))
        self.scale=QDoubleSpinBox()
        self.scale.setRange(0,100000)
        self.scale.setDecimals(3)
        self.scale.setSingleStep(1)
        self.scale.setSuffix(" px / m")
        self.scale.setValue(0)
        self.scale.valueChanged.connect(self.scale_changed)
        self.scale.setMaximumWidth(460)
        self.scale.lineEdit().setTextMargins(20, 0, 8, 0)
        outer.addWidget(self.scale)
        outer.addWidget(textlabel("Use a known-length object/segment in the same depth plane as the athlete. Recalibrate after zoom.",11,MUTED))
        outer.addSpacing(14)
        outer.addWidget(textlabel("DETECTION",11,MUTED,True))
        outer.addWidget(textlabel("Analyze every Nth frame",13,INK,True))
        self.duration=QSpinBox()
        self.duration.setRange(1,30)
        self.duration.setValue(4)
        self.duration.setSuffix(" frames")
        self.duration.setMaximumWidth(460)
        self.duration.lineEdit().setTextMargins(20, 0, 8, 0)
        outer.addWidget(self.duration)
        outer.addWidget(textlabel("Candidate sensitivity",13,INK,True))
        self.sensitivity=QSlider(Qt.Orientation.Horizontal)
        self.sensitivity.setRange(1,100)
        self.sensitivity.setValue(45)
        self.sensitivity.setMaximumWidth(460)
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

    def set_pan_mode(self, active):
        self.canvas.pan_mode=active
        self.pan_btn.setText("Pan: on" if active else "Pan: off")
        self.notice.setText("Pan ON: left-drag to move; turn off to click ruler marks." if active else "Pan OFF: left-click ruler marks; right-drag also pans.")

    def begin_ruler_calibration(self):
        if not self.cap:
            return
        self.timer.stop()
        self.mode="ruler"
        self._ruler_first=None
        self.notice.setText("Calibrate 50 cm: wheel to zoom, RIGHT-drag to pan, LEFT-click two ruler marks.")

    def canvas_clicked(self,x,y):
        if self.mode=="ruler":
            if self._ruler_first is None:
                self._ruler_first=(x,y)
                self.notice.setText("RIGHT-drag to reposition if needed, then LEFT-click the second mark.")
            else:
                distance=abs(y-self._ruler_first[1])
                self.mode=""
                if distance<30:
                    self.notice.setText("Marks too close. Zoom in and select two marks 50 cm apart.")
                    return
                self.scale.setValue(distance/self.reference_m.value())
                self.notice.setText(f"Calibrated: {distance/self.reference_m.value():.1f} pixels per metre (estimated)")
                self.update_display()
            return
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
        # Use the lightweight prototype video whenever it is available.
        candidates = [
            ROOT / "video" / "prototypev1.mp4",
            ROOT / "videos" / "prototypev1.mp4",
            ROOT / "prototypev1.mp4",
            ROOT / "video" / "prototype.mov",
            ROOT / "videos" / "prototype.mov",
            ROOT / "prototype.mov",
        ]
        for candidate in candidates:
            if candidate.is_file():
                self.load_video(str(candidate))
                return
        self.notice.setText("Put prototypev1.mp4 in the video folder or click Change video.")
        self.open_btn.setEnabled(True)

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
        self.tracks={}
        self.fixed_baseline=None
        self.auto_candidates=[]
        self.lip_a=self.lip_b=self.hip=None
        self.pixels_per_metre=0
        self.scale.blockSignals(True)
        self.scale.setValue(0)
        self.scale.blockSignals(False)
        self.read_sidecar()
        self.timeline.total=self.frames
        self.seek(0)
        self.setWindowTitle(f"Prototype V1.3 — {Path(filename).name}")
        # Restore tracking automatically for the lightweight prototype.
        # The 4K MOV stays manual so decoding/YOLO cannot freeze playback.
        if Path(filename).name.lower()=="prototypev1.mp4":
            self.notice.setText("MP4 ready. Loading or building YOLO skeleton tracking...")
            QTimer.singleShot(450, lambda: self.scan() if self.path==filename else None)
        else:
            self.notice.setText("4K video ready. Click Run detection to restore skeleton and measuring lines.")

    def seek(self,n):
        if not self.cap:
            return
        self.frame_index=max(0,min(self.frames-1,int(n)))
        if self._next_decode_index != self.frame_index:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.frame_index)
        ok,img=self.cap.read()
        self._next_decode_index=self.frame_index+1
        if not ok:
            self.notice.setText("Unable to read requested frame.")
            return
        self.canvas.frame=img
        self.update_display()

    def update_display(self):
        self.canvas.lip_a=self.lip_a
        self.canvas.lip_b=self.lip_b
        self.canvas.hip=self.hip
        self.canvas.pixels_per_metre=self.pixels_per_metre
        self.canvas.fixed_baseline=self.fixed_baseline
        if self.tracks:
            nearest=min(self.tracks,key=lambda k:abs(k-self.frame_index))
            self.canvas.pose=self.tracks[nearest] if abs(nearest-self.frame_index)<=max(2,self.duration.value()) else None
        else:
            self.canvas.pose=None
        self.canvas.update()
        self.timeline.current=self.frame_index
        self.timeline.jumps=self.jumps
        self.timeline.update()
        self.counter.setText(f"Frame {self.frame_index+1:,} / {self.frames:,}     {self.frame_index/self.fps:,.2f}s")
        current=next((j for j in self.jumps if j.frame==self.frame_index),None)
        if current is None and self.canvas.pose:
            px=self.canvas.pose.get("height_px")
            if px is None:
                self.measure.setText("Tape reference not found")
                return
            self.measure.setText(f"{px / self.pixels_per_metre:.2f} m · estimated" if self.pixels_per_metre > 0 else f"{px:.0f} px · uncalibrated")
            return
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            self.previous_frame()
            event.accept()
            return
        if event.key() == Qt.Key.Key_Right:
            self.timer.stop()
            self.play_btn.setIcon(svg_icon("play"))
            self.next_frame()
            event.accept()
            return
        if event.key() == Qt.Key.Key_Space:
            self.toggle_play()
            event.accept()
            return
        super().keyPressEvent(event)

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

    def scan(self,force=False):
        if not self.cap:
            self.notice.setText("Wait for the video or open your local MP4 first.")
            return
        self.timer.stop()
        self.scan_btn.setEnabled(False)
        self.rescan_btn.setEnabled(False)
        self.notice.setText("Loading saved tracking or analyzing video…")
        self.worker=Worker(self.path,self.pixels_per_metre,self.duration.value(),self.sensitivity.value()/100,force=force)
        self.worker.progress.connect(lambda p: self.notice.setText(f"Analyzing video… {p}%"))
        self.worker.finished_jumps.connect(self.scan_done)
        self.worker.failed.connect(self.scan_failed)
        self.worker.start()

    def scan_done(self,proposals):
        cached=isinstance(proposals,dict) and proposals.get("from_cache",False)
        if isinstance(proposals,dict):
            self.tracks=proposals.get("tracks",{})
            self.fixed_baseline=proposals.get("baseline")
            proposals=proposals.get("jumps",[])
        self.auto_candidates=list(proposals)
        manual=[j for j in self.jumps if j.source!="auto candidate"]
        manual_frames={j.frame for j in manual}
        filtered=[j for j in proposals if j.frame not in manual_frames and (self.pixels_per_metre<=0 or j.pixel_height is None or j.pixel_height/self.pixels_per_metre>=.05)]
        for j in filtered:
            j.height_m=metres_from_pixels(j.pixel_height,self.pixels_per_metre)
        self.jumps=sorted(manual+filtered,key=lambda j:j.frame)
        self.notice.setText(f"{'Loaded saved analysis' if cached else 'Analysis saved for next time'} · {len(proposals)} jump candidates. Calibrate ruler for metres.")
        self.scan_btn.setEnabled(True)
        self.rescan_btn.setEnabled(True)
        self.update_display()
        self.save_sidecar()

    def scan_failed(self,error):
        self.scan_btn.setEnabled(True)
        self.rescan_btn.setEnabled(True)
        QMessageBox.warning(self,"Tracking failed",error)
        self.notice.setText("Automatic analysis failed. Check the model installation or video.")

    def scale_changed(self,value):
        self.pixels_per_metre=value
        self.canvas.pixels_per_metre=value
        for jump in self.jumps:
            if jump.pixel_height is not None:
                jump.height_m=metres_from_pixels(jump.pixel_height,value)
        if hasattr(self,"auto_candidates") and self.auto_candidates:
            manual=[j for j in self.jumps if j.source!="auto candidate"]
            accepted=[j for j in self.auto_candidates if value<=0 or j.pixel_height is None or j.pixel_height/value>=.05]
            for j in accepted:
                j.height_m=metres_from_pixels(j.pixel_height,value)
            self.jumps=sorted(manual+accepted,key=lambda j:j.frame)
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
    if os.name == "nt":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("OliverWeiner.Halfpipe")
        except Exception:
            pass
    app.setStyle("Fusion")
    font_file=ROOT/"assets"/"Inter-Regular.ttf"
    if font_file.exists():
        QFontDatabase.addApplicationFont(str(font_file))
    app.setFont(QFont("Inter" if "Inter" in QFontDatabase.families() else "Segoe UI", 10))
    app.setStyleSheet("""
QWidget { background:#0c0e12; color:#e8eaf0; font-family:Inter,'Segoe UI',sans-serif; font-size:12px; }
QFrame#side { background:#111318; border-right:1px solid #292c35; }
QFrame#side QLabel { background:transparent; }
QLabel#brand { color:#fafbff; font-size:17px; font-weight:700; letter-spacing:1px; }
QLabel#version { color:#8a92a3; font-size:10px; }
QLabel#status { color:#9aa1b0; font-size:11px; }
QPushButton { background:#191c23; border:1px solid #303540; border-radius:9px; padding:8px 12px; color:#e9eaf0; }
QPushButton:hover { background:#2b303a; }
QPushButton:pressed { background:#373d4a; }
QPushButton:disabled { color:#666e7e; }
QPushButton#navButton { background:transparent; border:none; padding:0; }
QPushButton#navButton:hover { background:#20242d; }
QPushButton#navButton[selected="true"] { color:#fff; background:#282d37; font-weight:600; }
QPushButton#transport { padding:4px; border-color:#303540; }
QPushButton[primary="true"] { background:#e9ecf4; border-color:#e9ecf4; color:#151923; font-weight:600; }
QPushButton[primary="true"]:hover { background:#cfd7e6; }
QDoubleSpinBox,QSpinBox { background:#171a21; color:#fafbff; border:1px solid #373c48; border-radius:9px; min-height:42px; padding-left:24px; padding-right:37px; selection-background-color:#4b5771; }
QDoubleSpinBox::up-button,QSpinBox::up-button { subcontrol-origin:border; subcontrol-position:top right; width:29px; background:#272c36; border-left:1px solid #444c5b; border-top-right-radius:8px; }
QDoubleSpinBox::down-button,QSpinBox::down-button { subcontrol-origin:border; subcontrol-position:bottom right; width:29px; background:#272c36; border-left:1px solid #444c5b; border-bottom-right-radius:8px; }
QDoubleSpinBox::up-arrow,QSpinBox::up-arrow { image:url(assets/arrow-up.svg); width:10px; height:10px; }
QDoubleSpinBox::down-arrow,QSpinBox::down-arrow { image:url(assets/arrow-down.svg); width:10px; height:10px; }
QScrollArea { border:none; background:#0c0e12; }
QScrollBar:vertical { background:#13161c; width:7px; }
QScrollBar::handle:vertical { background:#353c4a; border-radius:3px; min-height:20px; }
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical { height:0; }
QSlider::groove:horizontal { height:5px; background:#323947; border-radius:2px; }
QSlider::handle:horizontal { width:17px; margin:-6px 0; background:#dce3f1; border-radius:8px; }
QCheckBox { spacing:12px; }
    """)
    win=App()
    win.setWindowIcon(image_icon("app-icon"))
    win.show()
    if os.name == "nt":
        try:
            import ctypes
            flag = ctypes.c_int(1)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(int(win.winId()), 20, ctypes.byref(flag), 4)
            color = ctypes.c_int(0x00120F0C)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(int(win.winId()), 35, ctypes.byref(color), 4)
        except Exception:
            pass
    app.exec()

if __name__=="__main__":
    main()
