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
WHITE = "#0c0e12"
INK = "#f3f5f8"
MUTED = "#9aa2b1"
ACCENT = "#c4cce0"
BORDER = "#282d36"

# Inline, scale-independent line icons.
ICONS = {
    "home": '<path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1Z"/><path d="M9 21v-8h6v8"/>',
    "settings": '<path d="M10 2h4l.7 2.2 2.1.9 2-.9 2.8 2.8-.9 2 1 2.2L23 11v4l-2.3.7-.9 2.1.9 2-2.8 2.8-2-.9-2.2 1L14 25h-4l-.7-2.3-2.1-.9-2 .9-2.8-2.8.9-2-.9-2.2L0 15v-4l2.3-.7.9-2.1-.9-2 2.8-2.8 2 .9 2.2-1Z" transform="translate(2 1) scale(.8)"/><circle cx="12" cy="12" r="3.2"/>',
