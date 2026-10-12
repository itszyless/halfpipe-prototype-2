# Halfpipe prototype-2

A small Python desktop app for checking the height of a selected jump frame above the blue line of a halfpipe.

This first version is manual. You choose the peak frame and click the lip and hip. It measures a vertical gap in the image. It does not detect athletes, find jumps, or process a live broadcast automatically.

## Start on Windows

Install Python 3.12 from [python.org](https://www.python.org/downloads/). Include Tcl/Tk and pip in the installer. Open PowerShell in this project folder, then run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py examples/demo.mp4
```

You do not need to activate the environment. To open the app without the demo:

```powershell
.\.venv\Scripts\python.exe app.py
```

Tested with Python 3.12 on Windows. The measurement checks use Python's built-in test tools:

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```

## Try the demo first

The included demo is a generated drawing. It is not real footage or a real height measurement.

1. Move the slider to frame 15. Frames start at 0.
2. Click the blue line at `(200, 400)` and `(760, 400)` in the video image. These are lip A and lip B.
3. Click the red hip dot at `(480, 160)`.
4. The status should show `240.0 px`.
5. For this demo only, enter `80` in Pixels/metre. Save jump `1`.
6. The row should show `3.0` metres because `240 / 80 = 3`.
7. Click Export CSV and choose where to save it. Compare it with [the example export](examples/demo-result.csv).

The numbers above are image coordinates. The top toolbar is outside the video image.

## Use your video

1. Choose Open video for a local file, or Open link for a direct video URL.
2. Use the slider to find a jump. Use Previous and Next to compare nearby frames. The other two buttons move by 30 frames.
3. Choose the frame where the hip looks highest above the nearby lip. This choice is yours. The program does not find the peak.
4. Click two points on the same local section of the blue line. The hip must be horizontally between the points. Do not connect the opposite sides of the pipe.
5. Click the centre of the hip. This is a visual hip reference, not a full body centre of mass calculation.
6. Leave Pixels/metre empty unless you have a valid local scale for that frame.
7. Give the jump a label and click Save/replace jump.
8. Use a different label for the next jump. Saving the same label for the same video replaces its previous row.
9. Export CSV before closing. Rows are kept in memory and are lost when the app closes. There is no CSV import yet.

Moving to another frame clears the points and the scale. Mark the lip again because the camera can move. Reset points clears the clicks on the current frame. It keeps the current scale, so recheck it if you choose a different section.

The window is fixed at about 960 by 875 screen pixels. On a small screen, reduce Windows display scaling or use a larger display. The table shows about five rows at once; CSV export contains all saved rows.

## What the result means

Pixels are the small squares in a video image. The app keeps measurements in the original video resolution even when it shows a smaller preview.

Image coordinates start at the top left. X increases to the right. Y increases downwards. The two lip clicks define a straight local line:

```text
lip_y = y1 + (y2 - y1) * (hip_x - x1) / (x2 - x1)
height_px = lip_y - hip_y
height_m = height_px / pixels_per_metre
```

A positive number means the hip is above the line in the image. A negative number means it is below. This uses the image's vertical direction. It is not a perpendicular distance to the lip, and it is not automatically the real vertical direction.

For example, if a known vertical reference of 2 metres covers 160 pixels in the original frame, its scale is `160 / 2 = 80` pixels per metre. The reference must be near the athlete, at a similar depth, and aligned with the direction being measured. A horizontal pipe width or an athlete's guessed height is not enough. Do not measure the reduced preview and then use its pixels as original pixels.

A single camera loses depth information. Perspective, camera tilt, curved lips, zoom, and motion can all change the scale. Mark a short local lip section rather than treating the whole pipe as a straight line. Metre values are rough estimates under those assumptions. Leave the scale empty if it is unknown. This prototype is not ready for judging.

The sample event link was opened and its first frame was decoded during development. The full file is about 17.4 GB. It is not included here. Direct links can be slow to seek. The app uses a 10 second open timeout and a 5 second read timeout where the video backend supports them. Loading can briefly pause the window. Short local clips are easier to use. Videos need a readable frame count and frame rate. The `seconds` column assumes a constant frame rate and can be approximate for variable frame rate footage.

## CSV columns

| Column | Meaning |
| --- | --- |
| video | Filename or final part of the direct link |
| jump | Your jump label |
| frame | Selected frame number, starting at 0 |
| seconds | Frame number divided by the reported frame rate |
| height_px | Signed image vertical gap in original pixels |
| height_m | Optional rough estimate in metres, blank if scale is unknown |
| pixels_per_metre | Scale used for this row, blank if unknown |
| lip_a_x, lip_a_y | First lip click in original pixels |
| lip_b_x, lip_b_y | Second lip click in original pixels |
| hip_x, hip_y | Hip click in original pixels |

## Files and learning

- [app.py](app.py): the window, video reading, clicks, saved rows, and CSV export.
- [measurement.py](measurement.py): the formula and input checks.
- [test_measurement.py](test_measurement.py): nine checks of the formula.
- [docs/BEGINNER_GUIDE.md](docs/BEGINNER_GUIDE.md): basic Python ideas and how the app works.
- [docs/LINE_BY_LINE.md](docs/LINE_BY_LINE.md): every line of the three Python files explained.
- [docs/PROTOCOL.md](docs/PROTOCOL.md): short work summary.
- [docs/HOURS.md](docs/HOURS.md): empty table for your real working hours.
- [docs/TESTING.md](docs/TESTING.md): what was checked and what still needs checking.

Python handles the logic, OpenCV reads video frames, Tkinter builds the window, and Pillow puts frames into that window. No account or paid service is needed to run it.

The video frame controls follow the [OpenCV VideoCapture documentation](https://docs.opencv.org/4.10.0/d8/dfe/classcv_1_1VideoCapture.html) and [frame position definitions](https://docs.opencv.org/4.12.0/d4/d15/group__videoio__flags__base.html).

## Next steps

Get a short clip with known jump heights and camera information. Compare repeated manual measurements with those references. After that, consider athlete tracking and automatic peak selection.

Development is on `prototype-2`. It has not been merged into `main`.
