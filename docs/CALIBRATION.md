# How to obtain metres

The app supports metre estimates for a selected jump. It cannot infer an absolute physical scale from pixels alone. The required input is a known vertical reference near that athlete at the same local depth, or a calibrated camera/scene model that establishes the equivalent relationship.

## In the app

1. Review the detected hip and lip. Correct them first if necessary.
2. Enter the confirmed vertical reference length in metres.
3. Click Calibrate this jump and mark the reference's top then bottom.
4. The table and selected-jump value show the estimate in metres. The JSON and CSV retain the reference points, length, scale, and projected gap.
5. Recalibrate when the camera, zoom, perspective, or athlete depth changes. A reference far in front of or behind the athlete gives a different scale.

Correcting hip/lip points clears the previous metre estimate. Reviewing a row does not validate its calibration. A high pose score does not validate a scale.

## Can the blue lines supply the distance?

Only when their real spacing is confirmed and the scene geometry makes them a suitable reference. The [FIS 2024 course-marking rule, section 3102.1.1](https://assets.fis-ski.com/f/252177/x/7224a970bb/sbfsfk-new-icr-spring-2024_clean.pdf) allows coloured markings on lips, transitions, and other features. That section does not assign a universal metre spacing to the visible blue stripes.

[WinSport's account of its pipe construction](https://www.winsport.ca/blog/2022-winsports-halfpipe-a-cut-above-thanks-to-team-effort/) describes a 22-foot cutter. That nominal pipe size does not identify two particular points in this recording or determine vertical scale at an airborne athlete. The curved wall, pipe inclination, and camera perspective prevent a simple universal pixel ratio.

## Information to request from the company

- Surveyed positions and real spacing of reference marks, with their directions.
- Camera intrinsics, distortion, lens/zoom settings, and camera positions/orientations, including changes during filming.
- The intended definition of vertical jump height and the lip location corresponding to the athlete.
- Labelled example jumps with independently measured physical heights and uncertainty.

The two-point tool is a local approximation for a known vertical reference. It is not full camera calibration, 3D reconstruction, or a validated judging measurement. No unverified blue-line distance is inserted into the real results.
