# Welcome to Lip

This version analyses real video automatically. It finds people and hip landmarks, fits a local blue lip, and groups above-lip measurements into candidate jumps. Every candidate needs review.

## Start an analysis

Choose Browse video, paste a direct video link, or drop a local video onto the window. Open Scan options to set Start and End in seconds for a short test. End 0 means the whole video. Click Scan video. Stop saves partial results.

The default fast pass uses two samples per second. Six is useful for checking a short run in more detail. Higher sampling catches more detail but takes longer. The peak is a robust sampled measurement, so the exact apex can fall between samples.

## Review results

Select a candidate in the table or click the timeline. Yellow shows the hip and its image vertical gap. Blue shows the detected local lip. Green shows the person and visible pose connections.

Check that the selected person is the athlete and that the blue line follows the lip near that athlete. A spectator, shadow, interior blue stripe, or camera cut can confuse the detector. The evidence score measures detection support; it is not the probability that the height is correct.

Use Correct points to open the original peak frame. Click lip A, lip B, and the hip. To add a missed peak, set its source time and click Add missed jump, then place the three points. Mark reviewed keeps a checked candidate. Exclude marks a false detection. Excluded rows stay in exports so the review history is visible.

## Understand height

The automatic result is an image vertical gap in pixels of the analysed video. Pixels from a resized copy differ from pixels in the original. The session records its video resolution.

The main table displays metres after calibration. Enter a known vertical reference length in metres and click Calibrate this jump. Click its top then bottom in the original frame. It must be a vertical reference near the athlete at the same depth. The app uses the reference direction and scale for that peak only. Uncalibrated rows show Calibrate. Blue marks are useful only if their real spacing and direction are confirmed. Zoom, tilt, and perspective can invalidate a scale. This prototype does not yet measure judging-ready real-world height automatically.

## Your files

Each analysis saves report.json, jumps.csv, peak snapshots, and a marked review video when the codec is available. Open results folder shows the session. Open session reloads report.json. The original video is read, not uploaded. Detection runs locally. The source-code version may download about 14 MB of model weights once. The packaged app includes them.

Closing during analysis requests a stop and waits for the current video read, then saves partial work. Moving the original video prevents correction until it is available again. Snapshots still work.

## Source and notices

Source and build instructions are on the public [prototype-2 branch](https://github.com/itszyless/halfpipe-prototype-2/tree/prototype-2). Dependency notices are included in docs/licenses.

## Runs and drop-ins

The table numbers riding sequences as runs. A gap over 15 seconds between candidates starts a new sequence. This does not identify athlete names, and a replay can appear again.

A jump needs recent below-lip evidence before it rises above the lip. An initial drop-in from the deck is rejected. Missing approach evidence can also reject a true jump. The saved report and skipped.csv include rejected intervals; use Add missed jump when a real peak is missing.

The supplied pipe dimensions are 6.7 m high, 160 m long, and 22 m wide, with an 18-degree slope and an 81-degree wall inclination. Open Pipe dimensions to see them. The 6.7 m reference default must still be matched to a visible vertical span at the correct depth. The curved wall is not a straight vertical reference.
