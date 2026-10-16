# Halfpipe Jump Measurement Prototype

A Python desktop prototype by **Oliver Weiner** for testing automatic jump detection and estimated jump heights from video.

The first test uses a short video of Oliver's brother jumping beside a ruler and a blue floor reference line. The goal is to explore techniques that could later be adapted to freeski and snowboard halfpipe footage.

> **Prototype status:** Experimental. Person tracking, jump markers and height estimates can be wrong. This is a proof of concept, not a certified measurement tool.

## Requirements

- Windows 10 or 11 (the desktop app was developed for Windows)
- Python 3.12
- Internet access for the first YOLO model download
- A local test video

## Setup

Open PowerShell in the project folder and run:

```powershell
git clone https://github.com/itszyless/halfpipe-prototype-2.git
cd halfpipe-prototype-2
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If you already cloned the project, use `git pull` instead of cloning it again.

## Add the video

Put the video in the `video` folder:

```text
halfpipe-prototype-2/
├── app.py
├── automatic.py
├── measurement.py
├── requirements.txt
└── video/
    ├── prototypev1.mp4
    └── prototype.mov       # optional higher-resolution version
```

The app prefers **`video/prototypev1.mp4`**. If this file is missing, it tries `prototype.mov`. Use **Change video** to open another recording.

The footage is not included in the public repository. Please only share recordings when everyone shown has agreed.

## Start

```powershell
.\.venv\Scripts\python.exe app.py
```

After an update:

```powershell
git pull
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

## Using the prototype

1. Open the default video or select your own.
2. Use **Play**, the timeline or **Left/Right arrow keys** to move through frames. Press **Space** to pause or resume.
3. The app uses **YOLO pose detection** to track the person and propose jump positions. The visible skeleton and guides depend on successful tracking.
4. Select **Calibrate ruler** and choose two ruler marks with a known distance. The default is **50 cm (0.50 m)**, adjustable in Settings.
5. Use the **mouse wheel** to zoom, **right-click and drag** to pan, and **left-click** to choose the marks. **Reset zoom** returns to the full view. If right-drag is unreliable, toggle **Pan** and left-drag, then turn Pan off before selecting marks.
6. Review the suggested jump markers and heights manually. The results are estimates.

## What is saved?

- Each video can have its own measurements JSON file.
- YOLO analysis is cached separately in a `.pose-cache.json` file next to the video.
- **Run detection** reuses a matching cache when available; **Reanalyze** runs the full analysis again.
- Changing the recording or detection settings can require a new analysis.
- Keep the cache file if you want to avoid repeating an expensive scan.

## How it works

- **OpenCV** reads the video frames.
- **Ultralytics YOLOv8 pose** finds body keypoints, including ankles and hips.
- Python and **NumPy** track vertical movement and estimate jump peaks.
- The reference line and ruler provide visual and approximate physical scale information.
- **PySide6** provides the desktop interface, playback controls, zoom, calibration and timeline.

## Current limitations

The detection can miss real jumps or mistake small steps for jumps. Ankles may be misplaced when the subject moves quickly. The blue tape detector is experimental. A ruler at a different depth from the athlete can distort the metres calculation. The camera angle, calibration and video quality all affect accuracy, and 4K playback can be slow. The project still needs validation against manually measured jumps.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Desktop interface, video playback, calibration and visualization |
| `automatic.py` | YOLO tracking, automatic jump candidates and analysis cache |
| `measurement.py` | Height calculations and jump data structures |
| `requirements.txt` | Python dependencies |
| `tests/` | Measurement tests |

**Author:** Oliver Weiner  
**Project:** Halfpipe jump height detection prototype  
**Technology:** Python, PySide6, OpenCV, YOLOv8, NumPy
