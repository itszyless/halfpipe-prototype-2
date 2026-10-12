# Testing notes

Checked on Windows with Python 3.12, OpenCV 4.14.0.94, and Pillow 12.3.0.

## Completed checks

- All nine automated measurement tests passed.
- The desktop app opened the included demo video.
- Moving the slider to frame 15 showed the demo peak.
- Clicking lip A `(200, 400)`, lip B `(760, 400)`, and hip `(480, 160)` showed `240.0 px`.
- Saving with the demo scale of 80 pixels per metre showed `3.0` metres.
- CSV export through the desktop window produced `examples/demo-result.csv` with the expected coordinates and numbers.
- The supplied event URL was opened separately with the same video backend. Its first frame decoded successfully. Reported frame rate was about 29.97 and frame count was 167044.

## Limits of these checks

The generated demo checks the controls and arithmetic. Its scale is invented for the example. It does not prove metre accuracy on real events. The full event video was not downloaded or measured end to end. Automatic detection, live streams, and camera calibration are not implemented. Other operating systems and variable frame rate timing have not been validated.

## Checks to do with the group

Use a short event clip with known jump heights. Mark the same jump several times and compare the spread of the results. Ask someone else to mark it too. Record camera zoom and angle changes. Confirm which lip section matches the athlete's location. Compare the peak frame choices before making claims about accuracy.
