"""Automatic pose and blue-lip jump candidate discovery.

Runs in a background thread. Requires ultralytics; first scan downloads
the small pose model. Camera motion/zoom can invalidate pixel-based heights.
"""
from pathlib import Path
import cv2
import numpy as np
from measurement import Jump, metres_from_pixels


def find_blue_lip(frame, x):
    """Find a likely blue line near a detected hip x coordinate.

    This is heuristic; painted snow and broadcast colors can confuse it.
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([90, 65, 65]), np.array([132, 255, 255]))
    h, w = mask.shape
    xx = max(0, min(w - 1, int(x)))
    half = max(6, round(w * .035))
    crop = mask[:, max(0, xx-half): min(w, xx+half)]
    scores = np.count_nonzero(crop, axis=1)
    if not scores.size:
        return None
    # Only accept a moderately continuous blue segment.
    y = int(np.argmax(scores))
    if scores[y] < max(3, crop.shape[1] * .16):
        return None
    return y


def analyze_video(path, scale=0, stride=4, sensitivity=.45, progress=None):
    """Detect hip keypoints and blue lip in sampled frames.

    Returns *candidate* peak events with a screen-space pixel height. The
    values are not reliable metres without scene-specific calibration.
    """
    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise RuntimeError("Install the updated requirements (ultralytics).") from exc
    model = YOLO("yolov8n-pose.pt")
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise RuntimeError("Unable to open the video")
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    stride = max(1, int(stride))
    observations = []
    prev_xy = None
    last_progress = -1
    try:
        for frame_no in range(0, n, stride):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ok, frame = cap.read()
            if not ok:
                break
            # Resize only for inference, then reproject coordinates to image.
            h, w = frame.shape[:2]
            ratio = min(1., 960. / max(h, w))
            small = cv2.resize(frame, (max(1,round(w*ratio)), max(1,round(h*ratio))))
            result = model.predict(small, conf=.30, imgsz=640, verbose=False, device="cpu")[0]
            candidates = []
            if result.keypoints is not None and result.keypoints.xy is not None:
                points = result.keypoints.xy.cpu().numpy()
                conf = result.keypoints.conf
                confidences = conf.cpu().numpy() if conf is not None else None
                for i, kps in enumerate(points):
                    if len(kps) <= 12:
                        continue
                    left, right = kps[11], kps[12]
                    if confidences is not None and min(confidences[i,11],confidences[i,12]) < .35:
                        continue
                    hip = (left + right) / (2 * ratio)
                    if np.all(np.isfinite(hip)) and hip[0] > 0 and hip[1] > 0:
                        blue_y = find_blue_lip(frame, hip[0])
                        if blue_y is None:
                            continue
                        px = max(0., float(blue_y - hip[1]))
                        candidates.append((float(hip[0]),float(hip[1]),px))
            if candidates:
                # Prefer continuity, otherwise strongest above-lip separation.
                selected = (min(candidates,key=lambda p:(p[0]-prev_xy[0])**2+
                           (p[1]-prev_xy[1])**2) if prev_xy is not None
                           else max(candidates,key=lambda p:p[2]))
                prev_xy = selected[:2]
                observations.append((frame_no,selected[2]))
            pct = int(100 * frame_no/max(1,n-1))
            if progress and pct != last_progress and pct % 2 == 0:
                progress(pct)
                last_progress = pct
    finally:
        cap.release()
    if len(observations) < 3:
        return []
    min_px = 12 + (1-float(sensitivity))*40
    gap = max(1,int(.9*fps))
    peaks = []
    for i in range(1,len(observations)-1):
        frame, val = observations[i]
        if val < min_px:
            continue
        if val < observations[i-1][1] or val < observations[i+1][1]:
            continue
        if peaks and frame-peaks[-1][0] < gap:
            if val > peaks[-1][1]:
                peaks[-1] = (frame,val)
        else:
            peaks.append((frame,val))
    return [Jump(int(f),metres_from_pixels(px,scale),float(px),"auto candidate")
            for f,px in peaks]
