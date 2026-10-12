# Work log

## Goal and scope

Build prototype-2 independently as a Python desktop program. Input is real halfpipe footage. Output is reviewable candidate jump times and signed hip-to-lip image gaps. The requested hip is used as a body reference, not a full biomechanical centre of mass.

## Work completed

- Replaced the initial manual-only window with an automatic video analysis pipeline.
- Inspected frames from the supplied Calgary freeski recording. The original stream is 1920 by 1080 at about 29.97 frames per second and lasts about 93 minutes.
- Made a local 960 by 540, 6-frame-per-second proxy to test the whole event without storing the roughly 17.4 GB original file. This changes resolution and sampling. Proxy pixels are not original pixels.
- Used an existing 17-point ONNX pose model with a fixed SHA-256 hash. Inference runs locally on the CPU. Side rotations provide additional hypotheses for difficult poses.
- Added a local colour boundary fit for the blue lip, camera-compensated motion ranking and temporal athlete selection, cut detection, grouping, and conservative peak selection.
- Added automatic session files, peak images, a silent marked review video, partial-run saving, review flags, exclusion, manual correction, missed-jump entry, and per-peak optional scale estimates.
- Built a native Qt window with a white interface, icon, timeline, results table, scrollable controls, and help tab.
- Added meaningful tests for geometry, missing evidence, cuts, isolated spikes, stop behaviour, files, and review actions.
- Wrote usage, learning, testing, protocol, attribution, and line-by-line documentation. Personal work hours remain for the student to fill in.

## What the experiments showed

The first 45 seconds produced six automatic candidate groups. Visual inspection showed useful hip/lip overlays, but also wrong person and wrong lip choices. A candidate count alone does not establish correctness. Rotation fallback changed some selected peaks. Peak smoothing was then tightened after a regression test exposed an isolated-spike problem.

The complete event scan is recorded in `TESTING.md`. It is a coverage and reliability check, not a benchmark against labelled ground truth.

## Important decisions

Metres are blank by default. The program cannot recover a reliable physical height from an arbitrary monocular broadcast image without camera calibration and appropriate scene information. A single body-height ratio or one pipe dimension was not used to manufacture a scale. The UI accepts an explicit local scale for a selected peak and labels the result an estimate.

No event footage, personal session, model weight, or packaged dependency binary is published in the source repository. The public branch contains the program, icon, tests, notices, and documentation. The packaged app and footage review remain local.

## Known limitations

Athlete selection is heuristic and can follow spectators. Pose landmarks can fail during rotations, blur, occlusion, and winter clothing. The top blue boundary can be a sign or a different pipe marking. A straight local fit approximates a curved projected lip. Image Y is not automatically the world vertical. Sampling can miss true apex frames. Scene cuts and long gaps can split one jump or join unrelated evidence. There is no validated athlete identity, trick classification, multi-camera reconstruction, real-time guarantee, or measured error bound.

## Next experiment

Label at least several complete runs with athlete identity, visible hip/lip points, and hand-checked peaks. Separate training footage from evaluation footage. Report false candidates, missed jumps, pixel error, timing error, and uncertainty. Ask the company for camera parameters, physical reference geometry, and their definition of physical vertical height before evaluating metre accuracy.

## Final revision

Renamed the desktop app to Lip and changed the interface to white with original SVG control icons. Fixed the packaged Qt startup failure by building with a restricted dependency search path. An unrelated Poppler ICU DLL had been bundled instead of allowing Qt to use the Windows ICU library. Added a centre crop and camera-compensated feature motion to reduce spectator selection. Retested the first real run and the original direct video link. Added a two-point local vertical reference for metre estimates, including tilted-reference tests.

## Motion regions, takeoff checks, and supplied geometry

Reproduced a wrong spectator selection in first-run frame 155. The original person passes missed the small sideways airborne rider. A camera-compensated moving crop with rotation passes recovered a rider hip near image coordinates (548, 129), while the standing spectator had near-zero residual motion. The first-run peak for that jump now marks the airborne rider. This is a verified example, not an event-wide accuracy result.

Added a below-lip takeoff requirement, a cut boundary check, a six-second maximum above-lip group, and saved rejected segments. Initial drop-ins lack below-lip takeoff evidence and are left out. The fast scan preserves strong single-frame moving candidates with an explicit warning. Candidate gaps over 15 seconds start new riding-sequence numbers. These numbers do not identify people or remove replays.

Stored the user-supplied course dimensions in reports. Added a 6.7 m reference default and explained why it still requires appropriate visible vertical endpoints. Simplified the white window to a compact status row, result table with run labels, and collapsed secondary settings. Added regression checks for drop-ins, scene cuts, sequence numbering, crop coordinate restoration, sparse motion, and fast-scan candidates.

## Complete revised event pass

Processed the complete 92.9-minute proxy with the moving-region detector: 11148 samples, 288 candidate groups after final regrouping, 158 skipped intervals, and 0 recorded decode errors. Saved run numbers, CSVs, images, and playback locally. Candidate contact images revealed remaining interior-stripe and person-selection errors. No claim of finding every real jump or producing validated event metre heights is made. Full counts and limitations are in TESTING.md.
