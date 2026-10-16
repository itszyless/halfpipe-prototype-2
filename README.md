## Indoor prototype video (October 2026)

The default footage is now the local **`prototypev1.mp4`**. Place it in `video/prototypev1.mp4` (or `videos/prototypev1.mp4`) within this repository. The app no longer starts a Calgary download. You can also click **Change video** to locate your file anywhere on the computer.

The 23-second portrait test has a floor-level blue reference line and a vertical ruler near the right edge. The existing pose-based hip detector and jump-candidate workflow are retained, and the line detector now searches the bottom portion of the image. **This is experimental and not verified against the real video results.** The ruler is not automatically interpreted: measurements in metres still need reliable scale calibration. Because perspective matters, a ruler at a different depth from the person can distort measurements.

Do not commit the video to this public repository unless you have permission to share the footage. `video/` and `*.mp4` are gitignored.

> **Update:** The latest code loads the Calgary video automatically (downloads it to the ignored `video/` folder on first launch) and includes pose-based automatic candidate detection with YOLO. It uses a background worker so the UI remains responsive. The first AI analysis downloads `yolov8n-pose.pt`; internet access is required. Run `pip install -r requirements.txt` again after pulling. A video can be loaded manually if the hosted link is inaccessible. Orange markers are AI-generated **unverified candidates**, not guaranteed jumps; a physically calibrated camera is still required for metre estimates. Inter is used when installed on the computer, otherwise Segoe UI. Basic UI fade transitions have been added. Large or long videos may analyze slowly on CPU.

# Prototype V1.2 — Halfpipe Jump Measurement

**Made by Oliver Weiner, 2EHIF.** Independent prototype-2 for reviewing freeski/snowboard halfpipe footage.

## Features

- Simple white PySide6 desktop interface, Inter font (when locally installed) with Home and scrollable Settings.
- Load an existing MP4/MOV/MKV/AVI from disk.
- Play/pause, move forward/backward exactly one decoded frame, and scrub the complete timeline.
- Mark two points along the **blue lip line**, select the skier's **hip centre** at the jump's peak, and save a jump.
- Green timeline markers for saved measurements, orange markers for *experimental* automatic jump candidates.
- Click a marker to jump to its video frame and inspect the reported pixels/metres.
- Enter **pixels per metre** under Settings. With no scale, results are displayed as pixels, **never fake metres**.
- Sidecar JSON for saved jumps and calibration, alongside the video.
- Experimental Lucas–Kanade optical-flow candidate discovery initiated by clicking a skier's hip on the current frame.

## Windows setup from scratch — VS Code

1. Install [Python](https://www.python.org/downloads/) (3.11 or 3.12 recommended). Enable **Add python.exe to PATH** during setup. On Windows, the Python launcher \`py\` is also fine.
2. Install [Visual Studio Code](https://code.visualstudio.com/) and the **Python** extension from Microsoft.
3. Install [Git for Windows](https://git-scm.com/download/win) or use VS Code's **Git: Clone** UI.
4. Open a terminal in VS Code (Terminal → New Terminal) and run:

   \`\`\`powershell
   git clone https://github.com/itszyless/halfpipe-prototype-2.git
   cd halfpipe-prototype-2
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   python app.py
   \`\`\`

   If Windows blocks PowerShell activation, either run
   \`Set-ExecutionPolicy -Scope Process Bypass\` first, or skip activation:
   \`.\.venv\Scripts\python.exe -m pip install -r requirements.txt\` and
   \`.\.venv\Scripts\python.exe app.py\`.
   
5. In VS Code choose **Python: Select Interpreter** → \`.venv\Scripts\python.exe\`.

6. Obtain the source video from the team (it is **not** included in GitHub). Use **Open video** to load the local MP4.

## Recommended presentation workflow

1. Open the local Calgary Camera 3 video.
2. Scrub to a clear frame with the athlete above the visible lip.
3. Click **Set lip line** and click two points on the relevant blue edge.
4. Click **Select hip** and click the athlete's hip centre.
5. If you have a **verified reference distance at the athlete's depth in that camera shot**, enter the measured scale in Settings (\`pixels_per_metre = reference_pixels / reference_metres\`).
6. Return Home and **Save jump**. The timeline displays a green dot.
7. Click the saved dot to review its value; repeat for jumps.
8. Optionally click **Find candidates** after selecting the hip to generate **unverified** orange markers, and review them manually.

**Important:** A single static scale is insufficient across camera zoom/pan/perspective changes; recalibrate where appropriate. The current prototype performs vertical *image-coordinate* distance measurements, not a full 3D world-space reconstruction. A true broadcast-grade system will require camera calibration and stable tracking of the athlete's hip and lip, potentially pose estimation plus camera-motion compensation. In the first version, motion detection is not equivalent to verified jump segmentation.

## Footage and external calibration background

Team-provided file:
\`https://s3.eu-central-1.wasabisys.com/judges/2025_26/freeski/Calgary%20(HP)/FK%20Finals%20-%201%20-%20Camera3%20-%20[10-30-18]%20[12-03-12].mp4\`

FIS's February 2025 Calgary World Cup results list the WinSport halfpipe wall height as **6.7 m**, halfpipe width as **22 m**, and length as **160 m** (2025 event). This is useful *physical-world context*, **not** enough to assert a pixel scale for this specific 2025/26 video.

Source: https://medias3.fis-ski.com/pdf/2025/FS/8076/2025FS8076RLF.pdf

The filename suggests a **2025/26 Calgary finals, Camera 3** video but the downloaded video and frame metadata have not been inspected in this environment.

## Data format

Each video generates \`yourfile.mp4.prototype-v1.2.json\`. This is ignored by Git. Jumps have the form:

\`\`\`json
{"frame": 240, "height_m": null, "pixel_height": 83.5, "source": "manual"}
\`\`\`

\`null\` metre heights mean no verified pixel-to-metre calibration was provided. Automatic candidates have no measurement values until verified.

## Known limitations / next steps

- Optical-flow detection may return false candidates (zoom, camera movement, skier occlusion, trick rotation). Only estimates candidate **peak frames**, not complete flights.
- The hip is manually marked for each measured frame; it is not currently maintained per-frame by a pose model.
- Lip reference is a line, assuming the two marked points represent the relevant visible lip; curved/oblique pipe geometry may need a more complex projection.
- An appropriate camera calibration is needed for geometrically valid metre measurements.
- Playback uses OpenCV frame seeking, which is generally accurate but may be slow for long high-resolution encoded video.
- The UI uses the Inter font when installed; the bundled code falls back to Segoe UI when it is not.
- No physical-video end-to-end tests have been performed yet. The test script checks calculation helpers only.

## Quick checks

\`\`\`powershell
python -m compileall -q app.py measurement.py
python -m unittest discover -s tests -v
\`\`\`

### Ruler calibration and floor tape (indoor clip)

In the Home view click **Calibrate ruler**. Click two marks **exactly 1.00 metre apart** on the yellow ruler, first and second, in the video frame. The measured distance sets pixels per metre and enables *approximate* metre readouts. If the ruler does not show two identifiable marks that far apart, do not guess; leave the measurement uncalibrated. The blue overlay is fixed to the pale floor tape detected near the lower edge of the first video frame. A separate standing-foot reference is used to calculate *jump displacement*: the foreground tape is not at the person's feet and therefore cannot be used as the foot takeoff y coordinate. The guide line toward the ruler is visual, not a full perspective correction. YOLO ankle detection can remain inaccurate when feet blur or leave the frame, so verify peak frames manually.

## Zoomable ruler calibration (latest)

On Home, use the **mouse wheel over the video** to zoom toward the cursor (up to 12×); **right-click and drag** to pan; choose **Reset zoom** to return to the full video. In Settings, enter the *actual distance in metres* between two readable marks on your ruler (for example 0.10 m for 10 cm). Back on Home, choose **Calibrate ruler**, zoom into the ruler and left-click those two marks. The coordinates are mapped back to the original frame, so zoom does not distort the calibration. A zoomed ruler offers more precise clicking, but cannot recover detail absent in the original recording.

**Limitations:** YOLO foot/ankle tracking and jumping peak estimation are not validated to guaranteed accuracy. A pixel-to-metre calibration can still be biased by depth/perspective. Confirm a few jump heights manually before treating results as reliable. The portrait indoor video is a test, not broadcast-grade halfpipe measurement.

## Saved YOLO analysis cache

The first successful detection saves a file next to the source video: `prototype.mov.pose-cache.json`. Subsequent app launches automatically reuse the cached YOLO skeleton coordinates and detected jump candidates, avoiding repeated 4K inference. The original full-resolution MOV is still used for video display and ruler zoom. Cache matching uses the video file size, modification time, detection stride, sensitivity and model version. Changing the video or either detection setting requires a fresh analysis. Ruler calibration changes do **not** invalidate the cache. **Run detection** reuses a valid cache; **Reanalyze** forces a full new scan and overwrites the cache. Keep the `.pose-cache.json` file if you want instant loading. The old per-video measurement `.json` is separate and unaffected.
