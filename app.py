"""Lip: automatic video analysis with a native review workspace."""

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PySide6.QtCore import QThread, Qt, QUrl, Signal
from PySide6.QtGui import QColor, QDesktopServices, QIcon, QImage, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import QApplication, QComboBox, QDoubleSpinBox, QFileDialog, QFrame, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QMainWindow, QMessageBox, QProgressBar, QPushButton, QScrollArea, QTabWidget, QTableWidget, QTableWidgetItem, QTextBrowser, QVBoxLayout, QWidget

from analysis import analyse, export_csv, open_video, save_report
from measurement import calibrate_height, measure_height
from vision import annotate, data_folder

ASSETS = Path(__file__).parent / 'assets'
STYLE = '''
QMainWindow, QWidget { background: #f7f9fc; color: #182334; font-family: 'Segoe UI'; font-size: 12px; }
QFrame#panel { background: #ffffff; border: 1px solid #e1e7ef; border-radius: 12px; }
QLabel { background: transparent; }
QLabel#muted { color: #64748b; }
QLabel#title { font-size: 28px; font-weight: 700; }
QLabel#metric { font-size: 27px; font-weight: 600; color: #2563eb; }
QPushButton { background: #e9eef6; border: 1px solid #dce4ef; padding: 9px 12px; border-radius: 7px; font-weight: 600; }
QPushButton:hover { background: #dbe7fb; }
QPushButton:disabled { color: #64748b; background: #f1f5f9; }
QPushButton#primary { background: #2563eb; color: #ffffff; border: none; }
QPushButton#primary:hover { background: #1d4ed8; }
QPushButton#danger { color: #b45343; }
QLineEdit, QDoubleSpinBox, QComboBox { background: #ffffff; border: 1px solid #dce4ef; border-radius: 6px; padding: 7px; selection-background-color: #bfd5ff; }
QProgressBar { background: #e9eef6; border: none; border-radius: 4px; height: 7px; }
QProgressBar::chunk { background: #2563eb; border-radius: 4px; }
QTableWidget { background: #ffffff; border: 1px solid #e1e7ef; gridline-color: #e9eef6; selection-background-color: #dce9ff; selection-color: #182334; }
QHeaderView::section { background: #f2f6fc; color: #55657b; padding: 9px; border: none; font-weight: 600; }
QTabWidget::pane { border: none; }
QTabBar::tab { background: #f7f9fc; color: #64748b; padding: 12px 20px; border-bottom: 2px solid transparent; }
QTabBar::tab:selected { color: #2563eb; border-bottom-color: #2563eb; }
QTextBrowser { background: #ffffff; border: none; padding: 18px; }
'''


def text_label(text, style=None):
    """Build a wrapping label with an optional named style."""
    label = QLabel(text)
    label.setWordWrap(True)
    if style:
        label.setObjectName(style)
    return label


def button(text, action, style=None):
    """Build a button and connect its click to one action."""
    control = QPushButton(text)
    control.clicked.connect(action)
    icon_name = {'browse': 'folder', 'open_session': 'folder', 'start_analysis': 'play', 'stop_analysis': 'stop', 'start_correction': 'edit', 'add_manual': 'plus', 'start_calibration': 'ruler', 'mark_reviewed': 'check', 'exclude': 'close', 'export_results': 'download', 'open_results': 'folder', 'open_review_video': 'play'}.get(action.__name__)
    if icon_name:
        if style == 'primary':
            icon_name += '-white'
        control.setIcon(QIcon(str(ASSETS / (icon_name + '.svg'))))
    if style:
        control.setObjectName(style)
    return control


class VideoCanvas(QLabel):
    """Show a fitted image and convert correction clicks to original pixels."""

    point_added = Signal(object)

    def __init__(self):
        super().__init__('Open a video to begin\n\nHip detection, local lip detection, and automatic jump candidates')
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(400, 240)
        self.setStyleSheet('background:#eef2f8; color:#718198; border:1px solid #e9eef6; border-radius:10px;')
        self.frame = None
        self.correcting = False
        self.points = []
        self.click_limit = 3

    def show_frame(self, frame):
        self.frame = frame.copy()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(rgb.data, rgb.shape[1], rgb.shape[0], rgb.strides[0], QImage.Format.Format_RGB888).copy()
        self.original = QPixmap.fromImage(image)
        self.setPixmap(self.original.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.frame is not None:
            self.show_frame(self.frame)

    def mousePressEvent(self, event):
        if not self.correcting or self.frame is None or len(self.points) >= self.click_limit:
            return
        ratio = min(self.width() / self.frame.shape[1], self.height() / self.frame.shape[0])
        offset_x = (self.width() - self.frame.shape[1] * ratio) / 2
        offset_y = (self.height() - self.frame.shape[0] * ratio) / 2
        x, y = (event.position().x() - offset_x) / ratio, (event.position().y() - offset_y) / ratio
        if 0 <= x < self.frame.shape[1] and 0 <= y < self.frame.shape[0]:
            self.points.append((x, y))
            self.point_added.emit(self.points.copy())


class HeightChart(QWidget):
    """Draw sampled gaps and let a click select the nearest candidate."""

    selected = Signal(int)

    def __init__(self):
        super().__init__()
        self.report = None
        self.setMinimumHeight(110)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor('#ffffff'))
        painter.setPen(QColor('#718198'))
        painter.drawText(16, 20, 'HIP ABOVE LIP  /  IMAGE PIXELS')
        if not self.report or not self.report['samples']:
            painter.drawText(16, 60, 'The measurement timeline appears after analysis.')
            return
        heights = [item['height_px'] for item in self.report['samples'] if item['height_px'] is not None]
        limit = max(50, float(np.percentile(np.abs(heights), 90))) if heights else 50
        begin, span = self.report['start'], max(0.01, self.report['end'] - self.report['start'])
        baseline = self.height() * 0.62
        painter.setPen(QPen(QColor('#d5ddea'), 1))
        painter.drawLine(16, round(baseline), self.width() - 16, round(baseline))
        path, connected = QPainterPath(), False
        samples = sorted(self.report['samples'], key=lambda item: item['time'])
        for sample in samples[::max(1, len(samples) // 1500)]:
            if sample['height_px'] is None or sample.get('cut'):
                connected = False
                continue
            x = 16 + (sample['time'] - begin) / span * (self.width() - 32)
            y = baseline - np.clip(sample['height_px'] / limit, -1, 1) * (self.height() * 0.32)
            if connected:
                path.lineTo(float(x), float(y))
            else:
                path.moveTo(float(x), float(y))
            connected = True
        painter.setPen(QPen(QColor('#2563eb'), 1.5))
        painter.drawPath(path)
        for jump in self.report['jumps']:
            x = 16 + (jump['peak_time'] - begin) / span * (self.width() - 32)
            painter.setBrush(QColor('#2563eb') if not jump['excluded'] else QColor('#a2acba'))
            painter.drawEllipse(round(x) - 3, round(baseline) - 3, 6, 6)
        painter.setPen(QColor('#718198'))
        painter.drawText(16, self.height() - 7, f'{begin:.1f}s')
        painter.drawText(self.width() - 80, self.height() - 7, f"{self.report['end']:.1f}s")

    def mousePressEvent(self, event):
        if self.report and self.report['jumps']:
            time = self.report['start'] + (event.position().x() - 16) / max(1, self.width() - 32) * (self.report['end'] - self.report['start'])
            index = min(range(len(self.report['jumps'])), key=lambda i: abs(self.report['jumps'][i]['peak_time'] - time))
            self.selected.emit(index)


class AnalysisWorker(QThread):
    """Keep video decoding and model inference off the window thread."""

    progress = Signal(object)
    preview = Signal(object)
    result = Signal(object)
    failed = Signal(str)

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def run(self):
        try:
            report = analyse(**self.settings, progress=self.progress.emit, preview=self.preview.emit, cancelled=self.isInterruptionRequested)
            self.result.emit(report)
        except InterruptedError:
            self.failed.emit('Stopped before analysis started. Existing sessions are safe.')
        except Exception as error:
            self.failed.emit(str(error))


class FrameWorker(QThread):
    """Read the original selected frame without blocking the window."""

    loaded = Signal(object)
    failed = Signal(str)

    def __init__(self, source, frame):
        super().__init__()
        self.source, self.frame = source, frame

    def run(self):
        capture = None
        try:
            capture, fps, count = open_video(self.source)
            capture.set(cv2.CAP_PROP_POS_FRAMES, self.frame)
            ok, image = capture.read()
            if not ok:
                raise ValueError('Could not load the original frame. Check that the video is still available.')
            self.loaded.emit(image)
        except Exception as error:
            self.failed.emit(str(error))
        finally:
            if capture is not None:
                capture.release()


class MainWindow(QMainWindow):
    """Own the controls, review canvas, result table, and session state."""

    def __init__(self):
        super().__init__()
        self.report = self.worker = self.frame_worker = None
        self.close_pending = False
        self.raw_frame = None
        self.pending_manual = None
        self.correction_mode = 'points'
        self.setWindowTitle('Lip | Prototype-2')
        self.setWindowIcon(QIcon(str(ASSETS / 'icon.ico')))
        self.resize(1220, 860)
        self.setMinimumSize(1020, 720)
        self.setAcceptDrops(True)
        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 18, 24, 18)
        header = QHBoxLayout()
        logo = QLabel()
        logo.setPixmap(QIcon(str(ASSETS / 'icon.svg')).pixmap(38, 38))
        header.addWidget(logo)
        header.addWidget(text_label('Lip', 'title'))
        header.addStretch()
        header.addWidget(text_label('HALFPIPE REVIEW  /  PROTOTYPE 2', 'muted'))
        layout.addLayout(header)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        workspace = QWidget()
        self.tabs.addTab(workspace, 'Analyse & review')
        body = QHBoxLayout(workspace)
        body.setContentsMargins(0, 12, 0, 0)
        left = QVBoxLayout()
        body.addLayout(left, 3)
        cards = QHBoxLayout()
        self.candidate_metric = self.card(cards, 'JUMPS TO REVIEW', '0')
        self.coverage_metric = self.card(cards, 'VISIBLE EVIDENCE', '0%')
        self.time_metric = self.card(cards, 'VIDEO SCANNED', '0:00')
        left.addLayout(cards)
        self.canvas = VideoCanvas()
        self.canvas.point_added.connect(self.correct_points)
        left.addWidget(self.canvas, 5)
        self.chart = HeightChart()
        self.chart.selected.connect(self.table_select)
        left.addWidget(self.chart, 1)
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(['Jump', 'Time', 'Height (m)', 'Image gap (px)', 'Status'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().hide()
        self.table.itemSelectionChanged.connect(self.show_selected)
        left.addWidget(self.table, 2)
        panel = QFrame()
        panel.setObjectName('panel')
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(340)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(panel)
        body.addWidget(scroll)
        right = QVBoxLayout(panel)
        right.setContentsMargins(18, 18, 18, 18)
        right.addWidget(text_label('Video', 'muted'))
        self.source = QLineEdit()
        self.source.setPlaceholderText('Choose video or paste direct link')
        self.source.setToolTip('You can also drop a local video onto the window.')
        right.addWidget(self.source)
        row = QHBoxLayout()
        row.addWidget(button('Browse video', self.browse))
        row.addWidget(button('Open session', self.open_session))
        right.addLayout(row)
        right.addWidget(text_label('Scan', 'muted'))
        right.addWidget(text_label('Times are in seconds. End 0 means the whole video.', 'muted'))
        row = QHBoxLayout()
        self.start = self.spin(row, 0, 999999, 'Start ')
        self.end = self.spin(row, 0, 999999, 'End ')
        right.addLayout(row)
        self.rate = QComboBox()
        for rate in (2, 4, 6, 10):
            self.rate.addItem(f'{rate} samples / second', rate)
        self.rate.setCurrentIndex(2)
        right.addWidget(self.rate)
        self.run_button = button('Analyse video', self.start_analysis, 'primary')
        right.addWidget(self.run_button)
        self.stop_button = button('Stop and save partial results', self.stop_analysis)
        self.stop_button.setEnabled(False)
        right.addWidget(self.stop_button)
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        right.addWidget(self.progress)
        self.status = text_label('Ready. Choose a video to start.', 'muted')
        right.addWidget(self.status)
        right.addWidget(text_label('Selected jump', 'muted'))
        self.details = text_label('Select a result to inspect its hip and lip marks.', 'muted')
        right.addWidget(self.details)
        self.correct_button = button('Correct lip and hip points', self.start_correction)
        right.addWidget(self.correct_button)
        row = QHBoxLayout()
        self.manual_time = self.spin(row, 0, 999999, 'Time ')
        row.addWidget(button('Add missed jump', self.add_manual))
        right.addLayout(row)
        self.height_metric = text_label('Set scale', 'metric')
        right.addWidget(self.height_metric)
        right.addWidget(text_label('Known vertical length near this jump', 'muted'))
        row = QHBoxLayout()
        self.reference_length = self.spin(row, 0.01, 100, '')
        self.reference_length.setValue(1)
        row.addWidget(text_label('metres', 'muted'))
        right.addLayout(row)
        right.addWidget(button('Calibrate this jump', self.start_calibration))
        row = QHBoxLayout()
        row.addWidget(button('Mark reviewed', self.mark_reviewed))
        row.addWidget(button('Exclude', self.exclude, 'danger'))
        right.addLayout(row)
        right.addWidget(text_label('Metres are estimates. Camera scale, depth, and tilt still need validation.', 'muted'))
        right.addStretch()
        right.addWidget(button('Export results CSV', self.export_results))
        right.addWidget(button('Open results folder', self.open_results))
        right.addWidget(button('Play marked review video', self.open_review_video))
        guide = QTextBrowser()
        guide.setOpenExternalLinks(True)
        guide.setMarkdown((Path(__file__).parent / 'docs' / 'APP_HELP.md').read_text(encoding='utf-8'))
        self.tabs.addTab(guide, 'How it works')
        self.load_recent()

    def card(self, layout, title, value):
        panel = QFrame()
        panel.setObjectName('panel')
        box = QVBoxLayout(panel)
        box.addWidget(text_label(title, 'muted'))
        label = text_label(value, 'metric')
        box.addWidget(label)
        layout.addWidget(panel)
        return label

    def spin(self, layout, minimum, maximum, prefix):
        control = QDoubleSpinBox()
        control.setRange(minimum, maximum)
        control.setDecimals(2)
        control.setPrefix(prefix)
        layout.addWidget(control)
        return control

    def browse(self):
        path, kind = QFileDialog.getOpenFileName(self, 'Open a video', '', 'Videos (*.mp4 *.mov *.mkv *.avi);;All files (*)')
        if path:
            self.source.setText(path)

    def start_analysis(self):
        if self.frame_worker and self.frame_worker.isRunning():
            self.status.setText('Wait for the peak frame to finish loading.')
            return
        source = self.source.text().strip().replace('https\\://', 'https://')
        if not source:
            self.status.setText('Choose a local video or paste a direct video link first.')
            return
        if self.worker and self.worker.isRunning():
            return
        self.worker = AnalysisWorker(dict(source=source, start=self.start.value(), end=self.end.value(), sample_rate=self.rate.currentData()))
        self.worker.progress.connect(self.update_progress)
        self.worker.preview.connect(self.canvas.show_frame)
        self.worker.result.connect(self.receive_report)
        self.worker.failed.connect(self.show_error)
        self.worker.finished.connect(self.analysis_finished)
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.correct_button.setEnabled(False)
        self.table.setEnabled(False)
        self.canvas.correcting = False
        self.progress.setValue(0)
        self.status.setText('Opening video and preparing the detector...')
        self.worker.start()

    def update_progress(self, data):
        self.progress.setValue(round(data.get('percent', 0)))
        seconds = data.get('time', 0)
        self.time_metric.setText(f'{int(seconds) // 60}:{int(seconds) % 60:02}')
        self.coverage_metric.setText(f"{100 * data.get('measured', 0) / max(1, data.get('samples', 0)):.0f}%")
        self.status.setText(data.get('message', '') + (f"\nAbout {data['remaining'] / 60:.1f} minutes remaining" if 'remaining' in data else ''))

    def stop_analysis(self):
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.status.setText('Stopping after the current video read. Saving partial results...')
            self.stop_button.setEnabled(False)

    def receive_report(self, report):
        self.report = report
        self.source.setText(report['source'])
        self.refresh_results()
        self.progress.setValue(100 if report['complete'] else 0)
        self.status.setText(f"{report['state'].replace('_', ' ').title()}. {len(report['jumps'])} candidates. Review before using results.")
        self.save_recent()
        if report['jumps']:
            self.table.selectRow(0)

    def analysis_finished(self):
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.correct_button.setEnabled(True)
        self.table.setEnabled(True)
        if self.close_pending:
            self.close()

    def refresh_results(self):
        report = self.report
        self.table.blockSignals(True)
        self.table.setRowCount(len(report['jumps']))
        for row, jump in enumerate(report['jumps']):
            state = 'Excluded' if jump['excluded'] else ('Reviewed' if jump['reviewed'] else 'Needs review')
            values = [str(jump['id']), f"{jump['peak_time']:.2f}s", 'Set scale' if jump['height_m'] is None else f"{jump['height_m']:.2f} m", f"{jump['height_px']:.1f}", state]
            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(value))
        self.table.blockSignals(False)
        self.candidate_metric.setText(str(sum(not jump['excluded'] for jump in report['jumps'])))
        measured = sum(sample['height_px'] is not None for sample in report['samples'])
        self.coverage_metric.setText(f"{100 * measured / max(1, len(report['samples'])):.0f}%")
        last_time = max((sample['time'] for sample in report['samples']), default=report['start'])
        self.time_metric.setText(f'{int(last_time) // 60}:{int(last_time) % 60:02}')
        self.chart.report = report
        self.chart.update()

    def selected_jump(self):
        row = self.table.currentRow()
        return self.report['jumps'][row] if self.report and 0 <= row < len(self.report['jumps']) else None

    def table_select(self, index):
        self.table.selectRow(index)

    def show_selected(self):
        jump = self.selected_jump()
        if not jump:
            return
        self.canvas.correcting = False
        self.canvas.points = []
        self.height_metric.setText('Set scale' if jump['height_m'] is None else f"{jump['height_m']:.2f} m")
        self.details.setText(f"Jump {jump['id']} at {jump['peak_time']:.2f}s\nEvidence score: {jump['confidence']:.0%}\n" + '\n'.join(jump['reasons']))
        snapshot = Path(self.report['folder']) / jump.get('snapshot', 'missing.jpg')
        if snapshot.exists():
            image = cv2.imread(str(snapshot))
            if image is not None:
                self.canvas.show_frame(image)

    def start_correction(self):
        jump = self.selected_jump()
        if not jump or (self.frame_worker and self.frame_worker.isRunning()):
            return
        self.status.setText('Loading the original peak frame for correction...')
        self.correct_button.setEnabled(False)
        self.frame_worker = FrameWorker(self.report['source'], jump['frame'])
        self.correction_jump = jump
        self.pending_manual = None
        self.correction_mode = 'points'
        self.table.setEnabled(False)
        self.frame_worker.loaded.connect(self.begin_correction)
        self.frame_worker.failed.connect(self.show_error)
        self.frame_worker.finished.connect(self.correction_loaded)
        self.frame_worker.start()

    def add_manual(self):
        if not self.report or (self.worker and self.worker.isRunning()) or (self.frame_worker and self.frame_worker.isRunning()):
            self.status.setText('Finish analysis or open a session before adding a missed jump.')
            return
        second = self.manual_time.value()
        if not self.report['start'] <= second < self.report['end']:
            self.status.setText('Choose a time inside this session range.')
            return
        self.correction_mode = 'points'
        self.pending_manual = dict(time=second, frame=round(second * self.report['fps']))
        self.correction_jump = None
        self.frame_worker = FrameWorker(self.report['source'], self.pending_manual['frame'])
        self.frame_worker.loaded.connect(self.begin_correction)
        self.frame_worker.failed.connect(self.show_error)
        self.frame_worker.finished.connect(self.correction_loaded)
        self.correct_button.setEnabled(False)
        self.table.setEnabled(False)
        self.frame_worker.start()

    def correction_loaded(self):
        self.correct_button.setEnabled(True)
        self.table.setEnabled(True)

    def begin_correction(self, frame):
        self.raw_frame = frame
        self.canvas.show_frame(frame)
        self.canvas.points = []
        self.canvas.correcting = True
        self.canvas.click_limit = 2 if self.correction_mode == 'scale' else 3
        if self.correction_mode == 'scale':
            self.status.setText('Click the top then bottom of the known vertical reference. Use the same depth as the athlete.')
            return
        self.status.setText('Click lip A, lip B, then the centre of the hip. Lip points must bracket the hip.')

    def correct_points(self, points):
        if self.pending_manual is None and self.selected_jump() is not self.correction_jump:
            self.canvas.correcting = False
            return
        marked = self.raw_frame.copy()
        for point in points:
            cv2.circle(marked, tuple(map(round, point)), 6, (80, 225, 255), -1)
        self.canvas.show_frame(marked)
        if self.correction_mode == 'scale':
            if len(points) == 2:
                self.save_calibration(points)
            return
        if len(points) != 3:
            self.status.setText(f"{len(points)} of 3 points set. Next: {['lip A', 'lip B', 'hip'][len(points)]}.")
            return
        try:
            gap, metres, lip_y = measure_height(*points)
        except ValueError as error:
            self.status.setText(str(error) + ' Click Correct to try again.')
            self.canvas.correcting = False
            return
        if self.pending_manual is not None:
            sample = dict(**self.pending_manual, person=dict(hip=list(points[2]), box=[points[2][0] - 20, points[2][1] - 30, 40, 60], points=[[0, 0, 0] for _ in range(17)], score=1.0, hip_score=1.0), lip=None, height_px=None, confidence=1.0, status='Manual measurement', cut=False, manual=True)
            jump = dict(id=max((item['id'] for item in self.report['jumps']), default=0) + 1, start=sample['time'], end=sample['time'], peak_time=sample['time'], frame=sample['frame'], height_px=gap, height_m=None, scale=None, confidence=1.0, reviewed=True, excluded=False, reasons=[], sample_index=len(self.report['samples']), manual=True)
            self.report['samples'].append(sample)
            self.report['jumps'].append(jump)
            self.refresh_results()
            self.table.selectRow(len(self.report['jumps']) - 1)
            self.pending_manual = None
        else:
            jump = self.correction_jump
        sample = self.report['samples'][jump['sample_index']]
        sample['person']['hip'] = list(points[2])
        sample['lip'] = dict(a=list(points[0]), b=list(points[1]), y=lip_y, score=1.0, extrapolated=False)
        sample['height_px'] = gap
        jump.update(height_px=round(gap, 2), height_m=None, scale=None, calibration=None, reviewed=True, corrected=True, reasons=['Points corrected manually. Camera scale is still uncalibrated.'])
        self.canvas.correcting = False
        jump['snapshot'] = f"jump-{jump['id']:03}-corrected.jpg"
        cv2.imwrite(str(Path(self.report['folder']) / jump['snapshot']), annotate(self.raw_frame, sample))
        self.persist()
        self.canvas.show_frame(annotate(self.raw_frame, sample))
        self.status.setText('Corrected points saved. Apply a valid scale only if it is known for this peak.')

    def start_calibration(self):
        jump = self.selected_jump()
        if not jump or (self.worker and self.worker.isRunning()) or (self.frame_worker and self.frame_worker.isRunning()):
            return
        self.correction_mode = 'scale'
        self.correction_jump = jump
        self.pending_manual = None
        self.frame_worker = FrameWorker(self.report['source'], jump['frame'])
        self.frame_worker.loaded.connect(self.begin_correction)
        self.frame_worker.failed.connect(self.show_error)
        self.frame_worker.finished.connect(self.correction_loaded)
        self.correct_button.setEnabled(False)
        self.table.setEnabled(False)
        self.status.setText('Loading the peak frame for a local metre reference...')
        self.frame_worker.start()

    def save_calibration(self, points):
        jump = self.correction_jump
        sample = self.report['samples'][jump['sample_index']]
        try:
            metres, scale, projected_gap = calibrate_height(sample['lip']['a'], sample['lip']['b'], sample['person']['hip'], points[0], points[1], self.reference_length.value())
        except ValueError as error:
            self.canvas.correcting = False
            self.status.setText(str(error) + ' Click Calibrate to try again.')
            return
        jump.update(height_m=round(metres, 3), scale=scale, calibration=dict(top=points[0], bottom=points[1], reference_metres=self.reference_length.value(), projected_gap_px=projected_gap, method='local_vertical_reference'))
        jump['reasons'] = [reason for reason in jump['reasons'] if not reason.startswith('Camera scale')]
        jump['reasons'].append('Local metre estimate. Reference depth and camera geometry need validation.')
        self.canvas.correcting = False
        self.persist()
        self.status.setText('Metre estimate saved for this jump. A changed camera or depth needs a new reference.')

    def mark_reviewed(self):
        jump = self.selected_jump()
        if jump:
            jump.update(reviewed=True, excluded=False)
            self.persist()

    def exclude(self):
        jump = self.selected_jump()
        if jump:
            jump.update(excluded=True, reviewed=True)
            self.persist()

    def persist(self):
        row = self.table.currentRow()
        try:
            save_report(self.report, self.report['folder'])
            export_csv(self.report, Path(self.report['folder']) / 'jumps.csv')
        except OSError as error:
            self.show_error(str(error))
            return
        self.refresh_results()
        if row >= 0:
            self.table.selectRow(row)

    def export_results(self):
        if not self.report:
            self.status.setText('Analyse a video or open a saved session first.')
            return
        path, kind = QFileDialog.getSaveFileName(self, 'Export jump results', 'jumps.csv', 'CSV (*.csv)')
        if path:
            try:
                export_csv(self.report, path)
                self.status.setText(f'Exported {Path(path).name}. Review and exclusion columns are included.')
            except OSError as error:
                self.show_error(str(error))

    def open_session(self):
        if (self.worker and self.worker.isRunning()) or (self.frame_worker and self.frame_worker.isRunning()):
            self.status.setText('Stop the current task before opening another session.')
            return
        path, kind = QFileDialog.getOpenFileName(self, 'Open report.json', str(data_folder() / 'sessions'), 'Session (*.json)')
        if path:
            self.read_session(path)

    def read_session(self, path):
        try:
            report = json.loads(Path(path).read_text(encoding='utf-8'))
            if report.get('version') != 2 or not isinstance(report.get('samples'), list) or not isinstance(report.get('jumps'), list):
                raise ValueError('This is not a supported Lip session.')
            report['folder'] = str(Path(path).parent)
            self.receive_report(report)
        except (OSError, ValueError, KeyError) as error:
            self.show_error(str(error))

    def open_results(self):
        folder = Path(self.report['folder']) if self.report else data_folder() / 'sessions'
        folder.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))

    def open_review_video(self):
        if self.report and (Path(self.report['folder']) / 'review.mp4').exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(Path(self.report['folder']) / 'review.mp4')))
        else:
            self.status.setText('No marked review video is available for this session yet.')

    def save_recent(self):
        if self.report:
            (data_folder() / 'recent.json').write_text(json.dumps(dict(report=str(Path(self.report['folder']) / 'report.json'))), encoding='utf-8')

    def load_recent(self):
        try:
            recent = json.loads((data_folder() / 'recent.json').read_text(encoding='utf-8'))
            if Path(recent['report']).exists():
                self.read_session(recent['report'])
        except (OSError, ValueError, KeyError):
            pass

    def show_error(self, message):
        self.status.setText(message)
        QMessageBox.warning(self, 'Lip', message)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        url = event.mimeData().urls()[0]
        self.source.setText(url.toLocalFile() if url.isLocalFile() else url.toString())

    def closeEvent(self, event):
        running = (self.worker and self.worker.isRunning()) or (self.frame_worker and self.frame_worker.isRunning())
        if running:
            self.close_pending = True
            self.stop_analysis()
            if self.frame_worker and self.frame_worker.isRunning():
                self.frame_worker.finished.connect(self.close)
            event.ignore()
        else:
            event.accept()


if __name__ == '__main__':
    application = QApplication(sys.argv)
    application.setStyle('Fusion')
    application.setStyleSheet(STYLE)
    window = MainWindow()
    if len(sys.argv) > 1:
        if sys.argv[1].endswith('.json'):
            window.read_session(sys.argv[1])
        else:
            window.source.setText(sys.argv[1])
    window.show()
    sys.exit(application.exec())
