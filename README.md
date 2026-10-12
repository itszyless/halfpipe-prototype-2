# Lip

Prototype-2 for reviewing halfpipe jumps from real video. The Python program samples the selected video range, finds body landmarks and a local blue lip, and groups above-lip measurements into jump candidates. It has a native Windows desktop window with a timeline, peak images, review controls, and CSV export.

This is a research prototype. A completed scan means the selected range was processed. It does not mean every jump was found or measured correctly. Spectators, flips, poor lighting, occlusion, camera cuts, and blue signs can cause errors. Review the marks before using a result. No detection accuracy or metre accuracy has been established.

## Use the desktop app

On the prepared computer, double-click the **Lip** desktop shortcut. The packaged app includes Python, the required libraries, and the pose model. Keep the app's `_internal` folder beside its executable.

1. Click **Browse video**, drop a local video onto the window, or paste a direct video link.
2. Open **Scan options** if you want a shorter range. Leave Start and End at 0 to process the whole video. For a first check, set End to 45 seconds.
3. Choose a sample rate in **Scan options**. The default is 2 for a faster whole-event pass. 6 samples per second gives a useful first pass. 2 is faster but can miss brief peaks. This is offline analysis; it is not guaranteed to run live.
4. Click **Scan video**. The window stays responsive while the background task runs. Review actions wait until it finishes.
5. Select each candidate. Inspect the athlete box, yellow hip point, blue lip, and yellow image gap.
6. Use **Correct points** if needed. Click lip A, lip B, and the hip. The two lip points must be on opposite horizontal sides of the hip.
7. Use the Time field and **Add missed jump** to measure a peak the detector missed. These entries are marked as manual.
8. Mark the candidate reviewed or exclude it. Export the table as CSV.

**Stop scan** ends after the current read and model call. Partial results remain available. **Open session** loads a saved `report.json`. Sessions reopen for review; the app does not resume an interrupted scan automatically.

## What the height means

Image coordinates start at the top left. Y increases downward. The program fits a short blue boundary near the athlete and evaluates its image Y coordinate at the hip's X coordinate.

`image gap in pixels = local lip Y - hip Y`

A positive value means the hip is above that fitted line in the picture. This is a signed image-space gap. It is not a measured physical vertical distance, a full centre-of-mass calculation, or height above the landing surface.

The main height column is in metres. Uncalibrated entries show **Calibrate**. For a metre estimate, select the jump, enter a known vertical reference length in metres, and click **Calibrate this jump**. Click the top then bottom of that reference in the original frame. The program uses the reference direction to intersect the lip through the hip, then divides that projected gap by pixels per metre. The reference must represent world vertical at the athlete's local depth. This estimate still assumes local camera projection and depth are valid. A single scale cannot be reused safely across camera pan, tilt, zoom, or changing depth. Known pipe dimensions alone do not solve this projection problem.

Candidate start/end are the first and last positive samples in a group, not exact takeoff and landing times. A candidate needs below-lip evidence within the preceding three seconds, without crossing a camera cut. This rejects the usual initial drop-in from the deck. Missing takeoff evidence can also reject a real jump; rejected segments remain in the report and skipped.csv. Extremely weak or stationary peaks are rejected too. At 2 samples per second, a strong moving single-frame candidate is retained with a sparse-evidence warning. Runs are separated by a pause over 15 seconds between candidates. Run labels are riding sequences, not athlete identities, and replays can appear again. Missing evidence is stored as `null`, not a zero-height jump. Evidence scores are heuristics, not calibrated probabilities. All automatic candidates start as **Needs review**.

## Supplied pipe dimensions

The session records the supplied values: wall height 6.7 m, length 160 m, width 22 m, slope 18 degrees, and wall inclination 81 degrees. The reference length starts at 6.7 m for convenience. Use that value only when two visible points represent the full vertical wall height at the rider's depth. A curved wall surface, pipe width, or two arbitrary blue stripes are not interchangeable with this vertical reference.

Known scene dimensions must be matched to visible image points and the camera's projection. The app does not silently assume those correspondences. See [OpenCV's camera model](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html) and `docs/CALIBRATION.md`.

## Saved files

Normal sessions are stored in `%LOCALAPPDATA%\Lip\sessions`.

| File | Purpose |
| --- | --- |
| `report.json` | Samples, settings, candidates, review decisions, and errors |
| `jumps.csv` | Candidate times, run numbers, pixel gaps, optional estimates, and review flags |
| `skipped.csv` | Rejected interval times and reasons for checking missed jumps |
| `jump-001.jpg` | Marked peak image for one candidate |
| `review.mp4` | Silent sampled playback with marks and source timestamps |

Review playback is written during analysis. Later manual corrections update the peak image, report, and CSV. They do not rewrite the full playback. Excluded rows remain in the CSV with an explicit exclusion flag. Store the source video and session together if moving them to another computer. A session contains a source path, not the source video itself.

## Run from Python

Use Python 3.12 on Windows. Open a terminal in this project folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If script activation is disabled, use `.venv\Scripts\python.exe` instead of `python`. No system setting change is needed. The source version downloads the verified 13.5 MB model once if it is not already present. Video and pose processing run locally. Direct video links and first model download require Internet access.

```powershell
python -m unittest -v
```

To build a Windows folder containing the app, run `build.ps1` from PowerShell after installing requirements. The build is platform specific. Source code and build instructions are provided on the `prototype-2` branch. No merge into `main` is needed.

## Project files

| File | Job |
| --- | --- |
| `app.py` | Native window, background tasks, review, and exports |
| `vision.py` | Verified model download, pose detection, athlete selection, and blue lip fitting |
| `analysis.py` | Video sampling, jump grouping, marked playback, and session files |
| `measurement.py` | Geometry for point corrections and a local vertical metre reference |
| `test_*.py` | Geometry, grouping, session, and review tests |
| `docs/BEGINNER_GUIDE.md` | Python basics and the complete data flow |
| `docs/LINE_BY_LINE.md` | Every Python source line explained |
| `docs/PROTOCOL.md` | Short work protocol |
| `docs/WORK_LOG.md` | Decisions, experiments, and current limitations |
| `docs/TESTING.md` | What was tested and what the tests do not prove |
| `docs/HOURS.md` | Blank personal time record |

## Next development step

Label athlete identities, blue lip points, and jump peaks in representative runs. Compare automatic results with those labels. Train or adapt a detector for this camera and winter clothing, improve tracking through flips, and calibrate the camera for physical heights. Until those steps are completed, this app is a review tool for candidate measurements.

## Dependencies and source

The pose model is [Xenova's ONNX export of YOLOv8n-pose](https://huggingface.co/Xenova/yolov8n-pose). Its export uses 17 body points; this program uses the hip points as the requested proxy. Window threading follows [Qt's QThread API](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QThread.html). See `THIRD_PARTY.md` and `LICENSE` for model attribution and dependency notices. The application source is provided under AGPL-3.0. The event footage and model weights are not stored in this repository.
