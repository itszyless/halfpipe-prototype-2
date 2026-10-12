# Start here

You do not need to understand everything at once. First run the app and review one candidate. Then read `measurement.py`, which is small. Next read `analysis.py`, then `vision.py`, and finally `app.py`. `LINE_BY_LINE.md` follows the exact source and explains each line.

## What Python does

A `.py` file is plain text containing instructions. Python reads the file from top to bottom. `import` makes another module available. A variable gives a name to a value, such as `gap = 50`. `=` stores a value; `==` compares values. A string is text in quotes. A number can be an integer, such as 6, or a decimal, such as 0.3. `True` and `False` are booleans. `None` means no value is available.

Indentation is part of Python's meaning. The indented lines below `if`, `for`, `while`, `with`, `try`, `def`, and `class` belong to that block. A colon starts the block. Blank lines make code easier to read but do not run anything. A comment starts with `#`. A triple-quoted string at the beginning of a module, function, or class is its documentation, called a docstring.

`def measure_height(...):` defines a function. A function is a reusable set of instructions. Defining it does not run its body. Calling `measure_height(a, b, hip)` supplies arguments and runs it. `return` sends a result back to the caller. A default argument, such as `pixels_per_metre=None`, can be left out by the caller.

A list holds ordered values: `[20, 150]` is a point with X then Y. Indexes start at 0. `points[0]` gets the first point. A tuple also holds ordered values and is often used for a fixed group. A dictionary stores named values: `jump['height_px']` gets the height under that key. `dict(height_px=50)` creates a dictionary. `**settings` passes dictionary keys as named function arguments. `*points` passes list elements as separate positional arguments.

`for item in items` repeats for each item. `while condition` repeats while the condition is true. `if condition` runs a block only when the condition is true. `continue` skips to the next loop step. `break` ends the loop. `range(3)` supplies 0, 1, and 2. A list comprehension such as `[x * 2 for x in values]` creates a list by repeating an expression.

`try` runs code that might fail. `except` catches a particular kind of failure. `raise ValueError(...)` reports invalid input. `finally` runs cleanup even when an error occurs. `with open(...)` closes a file when the block ends. A `lambda` is a short unnamed function. An f-string, such as `f'{gap:.1f}'`, puts a value into text; `:.1f` means one decimal place.

## Read the measurement with real numbers

Suppose lip A is `(100, 400)`, lip B is `(500, 440)`, and the hip is `(300, 250)`. The hip is halfway between the lip points in X. The fitted lip Y is therefore 420. The image gap is `420 - 250 = 170` pixels.

The formula first finds the hip's fraction along the lip: `(300 - 100) / (500 - 100) = 0.5`. It multiplies the lip's Y change by that fraction: `(440 - 400) * 0.5 = 20`. Adding that to the first lip Y gives 420. This is linear interpolation. It works with reversed lip points too.

If the scale really is 85 pixels per metre at this point, `170 / 85 = 2` metres. The arithmetic is easy. Establishing that this scale and image direction match physical height is the hard part. A tilted or moving camera changes the relationship. This program does not solve camera calibration.

The function rejects invalid numbers, a nearly vertical lip segment, a hip outside the two lip points, and a zero or negative scale. These checks prevent division by zero and unreasonable extrapolation. A negative signed gap is allowed because it means the hip is below the reference line.

## Follow one video frame

1. `analysis.py` opens the video and reads its frame rate and length. A frame is one still image. At 30 frames per second, frame 300 is about 10 seconds into the video.
2. It reads a sample and skips some intervening frames. Sampling reduces work. A sample rate of 6 means approximately six analysed images each second. The actual rate is `video_fps / stride`, because frame steps are whole numbers.
3. `vision.py` resizes the image to fit a 640 by 640 square and adds grey padding. It changes the colour order from OpenCV's BGR to RGB. It changes the array shape to batch, colour, height, width and divides the numbers by 255.
4. ONNX Runtime runs the pose model on the CPU. Its output contains possible person boxes, scores, and 17 body points. Overlapping boxes are filtered. Visible left and right hip points are combined with confidence weights. Moving crops are also tested at four rotations and mapped back to original image coordinates.
5. Optical flow tracks image features between samples. The strongest moving cluster becomes a magnified crop. This gives a small sideways rider more image detail. When motion cannot be estimated, a centre crop and side views provide a fallback. A robust affine transform estimates the background camera motion. Extra motion inside a person box increases its athlete ranking. Central position, prominence, and continuity also contribute. This is only a tracking heuristic. It can choose a spectator. It does not know an athlete's name or guarantee identity.
6. The lip detector changes the frame to HSV colour. Hue describes colour, saturation describes colour strength, and value describes brightness. A blue mask keeps pixels inside chosen colour limits.
7. Small blue components are removed. Near the hip, the detector takes the upper blue boundary at several X coordinates. It tries random line pairs and counts nearby supporting points. This robust fitting idea is called RANSAC. A final least-squares line is fitted to the strongest support. Sparse, narrow, or heavily extrapolated fits are rejected.
8. The lip Y minus the hip Y becomes the signed image gap. The weakest hip, person, or lip evidence contributes to the evidence score. If either the person or lip is missing, the gap stays `None`.
9. The sample goes into the report. A marked frame goes into the silent review video. The app gets a preview and a progress update.

## How samples become candidates

`find_jumps` keeps gaps larger than both 8 pixels and a fraction of the detected person's box height. It joins nearby positive samples, allows a brief missing gap, and starts a new group across a large time gap or a scene cut. A group normally needs at least two positive samples. In the fast 2-sample scan, a strong moving single-frame candidate is kept and explicitly flagged for a closer scan.

A candidate must have a negative below-lip sample within the previous three seconds and after the last scene cut. A rider already above the lip at the start of the shot therefore does not count as a takeoff. This rejects the initial drop-in, but can miss a jump when its approach is hidden. Rejected segments are saved for inspection. A pause over 15 seconds between candidates starts another numbered riding sequence. This does not recognise names or distinguish a replay.

A three-value median reduces the effect of a single spike. The peak is selected near the largest median value while favouring an actual sample consistent with its neighbours. This makes a reviewable peak image, but can miss the true maximum between sampled frames. Candidate timing is approximate.

Warnings explain uncertain choices. Calibration is always unresolved initially. A long group, an ambiguous person choice, an extended lip, a weak peak, or a group touching a range boundary gets a note. These notes help review; they do not prove an error is present or absent.

## Why the window stays responsive

A `class` describes a kind of object. An object holds data and methods. `self` means the current object. `MainWindow` is the app's window. `VideoCanvas` displays a frame. `HeightChart` draws the timeline. `super()` calls behaviour inherited from Qt's base class.

Qt calls event methods when something happens. A click emits a signal. `.connect(action)` connects the signal to a function. For example, the Scan video button calls `start_analysis`. The window then starts `AnalysisWorker`, a `QThread` subclass. Its `run` method performs the long scan in a background thread. Its signals carry progress, previews, and the finished report back to the window.

The worker does not change controls directly. Qt delivers the updates to the window thread. Stop requests an interruption; the scan checks it between work steps. A blocked network read may take up to its timeout before stopping. Closing during a scan requests a stop and waits for cleanup instead of abandoning an active thread.

## Corrections and files

The picture is scaled to fit the canvas. A mouse click gives window coordinates. `VideoCanvas` subtracts the letterbox offsets and divides by the display scale to recover original image coordinates. This is why resizing the window does not change the stored measurement.

Corrections load the original source frame in another worker. Three clicks call `measure_height`. The corrected peak gets a new snapshot and the metre estimate is cleared. A manually added candidate has its own selected source time and is labelled manual. Review decisions are saved immediately. The review video keeps its original automatic marks.

JSON stores nested dictionaries and lists in readable text. CSV stores a table that spreadsheet programs can open. OpenCV writes marked images and the sampled review video. A temporary JSON file is replaced only after it is fully written, so normal saves do not expose a half-written report. This is not a guarantee against a disk failure.

## Learning tasks

Try these in a copy of the project. Predict the result before running it.

1. Call `measure_height((0, 100), (200, 100), (100, 60))`. Explain why the gap is 40 and metres are `None`.
2. Move the hip Y to 120. Explain why the signed gap becomes negative.
3. Run the same short clip at 2 and 6 samples per second. Compare timing and missed peaks.
4. Exclude one candidate and open the CSV. Find the review and exclusion columns.
5. Explain why a 90% evidence score does not mean a 90% chance that a physical height is correct.
6. Trace the Scan video button through `start_analysis`, `AnalysisWorker.run`, `analyse`, and `receive_report`.

Useful reference: [Python's official tutorial](https://docs.python.org/3/tutorial/). The exact source lines are explained in `LINE_BY_LINE.md`; use this guide for the larger ideas.

## Metres and a tilted camera

`calibrate_height` uses a known vertical reference in the same frame as a selected jump. Click top then bottom. Their difference is a direction vector. `math.hypot(dx, dy)` gives its pixel length. Dividing by that length makes a unit vector. Dividing the reference's pixel length by its known metre length gives pixels per metre.

The hip plus an unknown distance times the unit vector describes a line following the visible vertical direction. The two lip points describe another line. The determinant is the 2D cross product used to solve where these lines meet. A small determinant means they are nearly parallel, so that geometry is rejected. The intersection must lie within the marked lip segment. The signed distance to that intersection divided by pixels per metre is the metre estimate.

Example: a visible vertical reference is 20 pixels long and is known to be 1 metre. The hip-to-lip distance along that direction is 60 pixels. The result is 3 metres. The tests use this known geometry. It does not establish a scale for the Calgary recording.

The blue marks in the event footage do not have a confirmed spacing in the supplied information. WinSport describes its pipe as 22 feet, but the wall is curved and the camera sees perspective. Dividing an arbitrary visible wall span by 6.7 metres would not establish a valid local vertical scale. Ask for surveyed reference marks or camera calibration before reporting measured physical heights. See CALIBRATION.md for sources and the remaining requirements.

## Follow the spectator fix

`motion_field` finds image corners, follows them into the next frame, and fits a translation/rotation/scale transform to the common background movement. It subtracts that predicted movement from each tracked point. A skier moving differently from the background has a larger residual.

`motion_regions` makes a mask around the strongly moving points and groups touching regions. It requires several supporting features, rejects huge regions and image edges, and takes the strongest remaining cluster. `PoseDetector.detect` magnifies that crop and tries four orientations. `restore_person` reverses both the rotation and crop offset, so all hips and boxes use the original video's pixels again.

`score_motion` measures residual motion inside each person box. `choose_athlete` combines it with position, size, model support, and continuity. In the difficult first-run frame, the airborne rider receives strong residual motion while the standing spectator receives almost none. This fixes that inspected case. Motion is still a heuristic, so another person moving near the pipe can confuse it.

The supplied course dimensions are saved as metadata. They are not a Python shortcut for camera calibration. Read CALIBRATION.md before changing a pixel result into metres.
