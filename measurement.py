"""Small, testable video measurement helpers for Prototype V1.2."""
from dataclasses import dataclass
import math
import cv2
import numpy as np


@dataclass
class Jump:
    frame: int
    height_m: float | None = None
    pixel_height: float | None = None
    source: str = "manual"

    def to_dict(self):
        return {"frame": self.frame, "height_m": self.height_m,
                "pixel_height": self.pixel_height, "source": self.source}


def metres_from_pixels(pixel_height, pixels_per_metre):
    if pixels_per_metre is None or pixels_per_metre <= 0:
        return None
    return max(0., float(pixel_height)) / float(pixels_per_metre)


def lip_y_at_x(a, b, x):
    """Interpolated image y coordinate on the selected lip reference line."""
    if a is None or b is None:
        return None
    x1, y1 = a
    x2, y2 = b
    if abs(x2 - x1) < 1e-6:
        return (y1 + y2) / 2
    return y1 + (y2 - y1) * ((x - x1) / (x2 - x1))


def pixel_height_above_lip(point, lip_a, lip_b):
    if point is None:
        return None
    lip_y = lip_y_at_x(lip_a, lip_b, point[0])
    if lip_y is None:
        return None
    return max(0., lip_y - point[1])


def track_candidates(path, start_frame, initial_point, scan_seconds=70, sensitivity=0.45,
                     progress=None):
    """Experimental optical-flow tracking. Never produces calibrated metre values.

    Track a point chosen on the skier across consecutive video frames. Peaks in
    upward screen motion are *candidates*, not validated jumps. Zoom/panning,
    occlusion, and rotation may cause false positives.
    """
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise RuntimeError("Cannot open video for tracking")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    first = max(0, min(int(start_frame), total - 1))
    last = min(total - 1, first + max(1, int(scan_seconds * fps)))
    cap.set(cv2.CAP_PROP_POS_FRAMES, first)
    ok, frame = cap.read()
    if not ok:
        cap.release()
        raise RuntimeError("Cannot read start frame")
    previous = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    point = np.array([[initial_point]], dtype=np.float32)
    samples = [(first, float(initial_point[1]))]
    window = max(1, last - first)
    for frame_i in range(first + 1, last + 1):
        ok, frame = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        nxt, status, _ = cv2.calcOpticalFlowPyrLK(
            previous, gray, point, None,
            winSize=(31, 31), maxLevel=3,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 25, 0.01))
        if nxt is None or not bool(status[0, 0]):
            break
        point = nxt
        samples.append((frame_i, float(point[0, 0, 1])))
        previous = gray
        if progress and (frame_i - first) % max(1, int(fps)) == 0:
            progress(int((frame_i - first) / window * 100))
    cap.release()
    if len(samples) < max(12, int(fps)):
        return []
    ys = np.array([v for _, v in samples], dtype=float)
    smooth_n = max(3, int(fps * .18) | 1)
    kernel = np.ones(smooth_n) / smooth_n
    smooth = np.convolve(np.pad(ys, (smooth_n//2, smooth_n//2),
                                mode="edge"), kernel, mode="valid")
    # Local upward extrema after meaningful vertical motion.
    threshold = 14 + (1 - float(sensitivity)) * 55
    min_gap = max(6, int(fps * 0.9))
    peaks = []
    for i in range(smooth_n, len(smooth) - smooth_n):
        if smooth[i] != min(smooth[i - smooth_n:i + smooth_n + 1]):
            continue
        left = smooth[max(0, i - int(fps)) : i + 1]
        right = smooth[i : min(len(smooth), i + int(fps) + 1)]
        if not len(left) or not len(right):
            continue
        if min(max(left) - smooth[i], max(right) - smooth[i]) < threshold:
            continue
        if peaks and i - peaks[-1] < min_gap:
            if smooth[i] < smooth[peaks[-1]]:
                peaks[-1] = i
            continue
        peaks.append(i)
    return [Jump(frame=samples[i][0], source="auto candidate") for i in peaks]
