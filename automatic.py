"""Experimental jump detection for the stationary 23-second indoor prototype.

Track ankle/foot height or the bottom of a detected person bounding box.
Do not require the blue floor line to overlap the subject. Distances
are screen-space estimates until physically calibrated.
"""
import cv2
import numpy as np
from measurement import Jump, metres_from_pixels


def find_blue_lip(frame, x=None):
    """Optional floor-line reference; never required for person detection."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]
    region = hsv[int(h * .60):]
    mask = cv2.inRange(region, np.array([85, 35, 35]), np.array([135, 255, 255]))
    scores = np.count_nonzero(mask, axis=1)
    if scores.size and scores.max() >= max(3, w * .08):
        return int(np.argmax(scores) + h * .60)
    return None


def find_jump_peaks(observations, fps, sensitivity=.45):
    """Find sustained upward foot movement from observed image y positions.

    observations: (frame number, lowest visible foot/bbox y) pairs.
    A peak is a *candidate*, not a validated jump or metre measurement.
    """
    if len(observations) < 5:
        return []
    frames = np.array([v[0] for v in observations], dtype=np.int32)
    bottoms = np.array([v[1] for v in observations], dtype=float)
    baseline = float(np.percentile(bottoms, 85))
    heights = np.maximum(0, baseline - bottoms)
    radius = 2
    smooth = np.convolve(np.pad(heights, (radius, radius), mode="edge"),
                         np.ones(2*radius+1)/(2*radius+1), mode="valid")
    min_height = 14 + (1 - float(sensitivity)) * 25
    min_gap = max(1, int(fps * .65))
    peaks = []
    for i in range(2, len(smooth)-2):
        if smooth[i] < min_height or smooth[i] < max(smooth[i-2:i+3]):
            continue
        # Require nearby frames to show a visible up/down motion.
        span = max(4, int(fps * .6 / max(1, np.median(np.diff(frames)))))
        lo = max(0, i-span)
        hi = min(len(smooth), i+span+1)
        if smooth[i] - min(np.min(smooth[lo:i+1]),np.min(smooth[i:hi])) < min_height*.5:
            continue
        if peaks and frames[i] - peaks[-1][0] < min_gap:
            if smooth[i] > peaks[-1][1]:
                peaks[-1] = (int(frames[i]), float(smooth[i]))
        else:
            peaks.append((int(frames[i]), float(smooth[i])))
    return peaks


def analyze_video(path, scale=0, stride=4, sensitivity=.45, progress=None):
    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise RuntimeError("Install dependencies: pip install -r requirements.txt") from exc
    model = YOLO("yolov8n-pose.pt")
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise RuntimeError("Cannot open video")
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    stride = max(1, int(stride))
    observations = []
    previous = None
    try:
        for frame_number in range(0, count, stride):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ok, frame = cap.read()
            if not ok:
                break
            h, w = frame.shape[:2]
            result = model.predict(frame, conf=.18, imgsz=640,
                                   verbose=False, device="cpu")[0]
            choices = []
            boxes = result.boxes.xyxy.cpu().numpy() if result.boxes is not None else []
            points = (result.keypoints.xy.cpu().numpy()
                      if result.keypoints is not None else [])
            confidence = (result.keypoints.conf.cpu().numpy()
                          if result.keypoints is not None and
                             result.keypoints.conf is not None else None)
            for i, box in enumerate(boxes):
                x1,y1,x2,y2 = map(float,box)
                if x2-x1 < w*.12 or y2-y1 < h*.12:
                    continue
                foot_y = y2
                if i < len(points) and len(points[i]) >= 17:
                    ankle_y = [float(points[i][k][1]) for k in (15,16)
                               if confidence is None or confidence[i][k] > .25]
                    if ankle_y:
                        foot_y = max(ankle_y)
                center = ((x1+x2)/2, (y1+y2)/2)
                choices.append((center,foot_y))
            if choices:
                selected = (min(choices,key=lambda v:(v[0][0]-previous[0])**2+
                                (v[0][1]-previous[1])**2) if previous is not None
                            else max(choices,key=lambda v:v[1]))
                previous = selected[0]
                observations.append((frame_number,selected[1]))
            if progress and frame_number % max(1,int(fps)) < stride:
                progress(min(100,int(frame_number*100/max(1,count))))
    finally:
        cap.release()
    peaks = find_jump_peaks(observations,fps,sensitivity)
    # Scale describes image-space screen distance, not true athlete's hip
    # height. Therefore do not supply a misleading number of metres.
    return [Jump(frame=frame,height_m=None,pixel_height=height,
                 source="auto candidate") for frame,height in peaks]
