"""Prototype YOLO pose tracking with jump apex detection.

Reference height: average grounded foot y from video, NOT arbitrary hip height.
True metric height requires ruler/camera calibration.
"""
import cv2
import json
import os
from pathlib import Path
import numpy as np
from measurement import Jump

# Standard COCO-17 keypoint skeleton connections
SKELETON = [(5,6),(5,7),(7,9),(6,8),(8,10),(5,11),(6,12),
            (11,12),(11,13),(13,15),(12,14),(14,16),(0,1),(0,2),
            (1,3),(2,4)]


def detect_tape_line(frame):
    """Locate pale blue/white tape low in the frame; not the wall edge.

    A short tape near the bottom is less saturated than conventional blue
    paint, so select the horizontally widespread pale band on red carpet.
    """
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    h,w=hsv.shape[:2]
    start=int(h*.86)
    roi=hsv[start:int(h*.97),:int(w*.83)]
    pale=(roi[:,:,1]<115)&(roi[:,:,2]>100)
    counts=np.count_nonzero(pale,axis=1)
    if not len(counts): return None
    # Require a continuous horizontal band across a substantial width.
    for i in np.argsort(counts)[::-1]:
        if counts[i]<max(24,int(w*.16)): continue
        xs=np.flatnonzero(pale[i])
        if len(xs)>1 and np.ptp(xs)>w*.50:
            return float(start+i)
    return None

def find_jump_peaks(observations, fps, sensitivity=.45, baseline=None):
    """Select highest measured feet position in each airborne interval."""
    if len(observations) < 5:
        return []
    frames = np.array([v[0] for v in observations], dtype=int)
    feet = np.array([v[1] for v in observations], dtype=float)
    # The ground reference is the lower foot location reached while standing.
    floor = float(baseline) if baseline is not None else float(np.percentile(feet, 90))
    raw_height = np.maximum(0, floor-feet)
    kernel = np.ones(5)/5
    smooth = np.convolve(np.pad(raw_height,(2,2),mode="edge"),kernel,mode="valid")
    cutoff = 12 + (1-float(sensitivity))*23
    airborne = smooth > cutoff
    events=[]
    start=None
    for i in range(len(airborne)+1):
        active = bool(airborne[i]) if i<len(airborne) else False
        if active and start is None:
            start=i
        elif not active and start is not None:
            end=i
            if end-start>=2:
                apex=start+int(np.argmax(smooth[start:end]))
                if smooth[apex]>=cutoff and (not events or frames[apex]-events[-1][0] >= fps*.45):
                    events.append((int(frames[apex]),float(raw_height[apex])))
            start=None
    return events


CACHE_VERSION=1


def _cache_file(path):
    return Path(str(path)+".pose-cache.json")


def _cache_key(path,stride,sensitivity):
    stat=Path(path).stat()
    return {"version":CACHE_VERSION,"size":stat.st_size,
            "mtime_ns":stat.st_mtime_ns,"stride":int(stride),
            "sensitivity":round(float(sensitivity),5),
            "model":"yolov8n-pose.pt"}


def _read_cache(path,key):
    try:
        cached=json.loads(_cache_file(path).read_text(encoding="utf-8"))
        if cached.get("key")!=key:
            return None
        payload=cached["data"]
        return {"jumps":[Jump(**j) for j in payload["jumps"]],
                "tracks":{int(k):v for k,v in payload["tracks"].items()},
                "baseline":payload.get("baseline"),
                "standing_y":payload.get("standing_y"),
                "from_cache":True}
    except (OSError,ValueError,KeyError,TypeError):
        return None


def _write_cache(path,key,data):
    target=_cache_file(path)
    temp=Path(str(target)+".tmp")
    payload={"key":key,"data":{"jumps":[j.to_dict() for j in data["jumps"]],
             "tracks":data["tracks"],"baseline":data["baseline"],
             "standing_y":data["standing_y"]}}
    try:
        temp.write_text(json.dumps(payload,separators=(",",":")),encoding="utf-8")
        os.replace(temp,target)
    except OSError:
        try:
            temp.unlink(missing_ok=True)
        except OSError:
            pass


def has_cached_analysis(path,stride=4,sensitivity=.45):
    try:
        return _read_cache(path,_cache_key(path,stride,sensitivity)) is not None
    except OSError:
        return False


def analyze_video(path, scale=0, stride=4, sensitivity=.45, progress=None, force=False):
    key=_cache_key(path,stride,sensitivity)
    if not force:
        previous=_read_cache(path,key)
        if previous is not None:
            if progress: progress(100)
            return previous

    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise RuntimeError("Install ultralytics using pip install -r requirements.txt") from exc
    model=YOLO("yolov8n-pose.pt")
    cap=cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise RuntimeError("Cannot read video")
    count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps=cap.get(cv2.CAP_PROP_FPS) or 30
    stride=max(1,int(stride))
    tracks={}
    observations=[]
    previous=None
    baseline=None
    try:
        for frame_no in range(0,count,stride):
            cap.set(cv2.CAP_PROP_POS_FRAMES,frame_no)
            ok,frame=cap.read()
            if not ok: break
            h,w=frame.shape[:2]
            if frame_no==0: baseline=detect_tape_line(frame)
            result=model.predict(frame,imgsz=640,conf=.16,verbose=False,device="cpu")[0]
            boxes=result.boxes.xyxy.cpu().numpy() if result.boxes is not None else []
            kps=result.keypoints.xy.cpu().numpy() if result.keypoints is not None else []
            conf=(result.keypoints.conf.cpu().numpy()
                  if result.keypoints is not None and result.keypoints.conf is not None else None)
            choices=[]
            for i, box in enumerate(boxes):
                x1,y1,x2,y2=map(float,box)
                if x2-x1 < w*.10 or y2-y1 < h*.10: continue
                pts=np.asarray(kps[i],dtype=float) if i<len(kps) else np.zeros((17,2))
                scores=conf[i] if conf is not None and i<len(conf) else np.zeros(17)
                visible=[j for j in (15,16) if scores[j]>.55 and pts[j,1]>0]
                foot=float(max(max(pts[j,1] for j in visible),y2-3)) if visible else y2
                center=((x1+x2)/2,(y1+y2)/2)
                choices.append((center,foot,pts.tolist(),scores.tolist()))
            if choices:
                selected=(min(choices,key=lambda q:(q[0][0]-previous[0])**2+(q[0][1]-previous[1])**2)
                          if previous is not None else max(choices,key=lambda q:q[1]))
                previous=selected[0]
                observations.append((frame_no,selected[1]))
                tracks[frame_no]={"points":selected[2],"conf":selected[3],
                                  "foot_x":selected[0][0],
                                  "foot_y":selected[1]}
            if progress and frame_no % max(stride,int(fps))<stride:
                progress(min(100,int(frame_no*100/max(1,count))))
    finally:
        cap.release()
    floor=baseline
    standing_y=float(np.percentile([v[1] for v in observations],90)) if observations else None
    events=find_jump_peaks(observations,fps,sensitivity,standing_y)
    for record in tracks.values():
        record["baseline_y"]=floor
        record["height_px"]=max(0.,standing_y-record["foot_y"]) if standing_y is not None else None
        record["standing_y"]=standing_y
    # Do not invent metres from a camera scale that hasn't been calibrated.
    jumps=[Jump(frame=f,height_m=None,pixel_height=px,source="auto candidate") for f,px in events]
    data={"jumps":jumps,"tracks":tracks,"baseline":floor,"standing_y":standing_y,"from_cache":False}
    _write_cache(path,key,data)
    return data
