# Testing record

Date: 2026-10-12. Windows 11, Python 3.12.14, CPU inference. Requirements are pinned.

## Automated checks

`python -m unittest -v`: 36 checks passed.

Tests cover signed pixel gaps, invalid coordinates/scales, upright and tilted known metre references, below-lip takeoffs, initial drop-ins, camera cuts, isolated spikes, weak wrong-person readings, separate riding sequences, strong single-frame fast-scan candidates, stationary peaks, crop rotation restoration, sparse motion features, blue-line fitting, source ranges, saved JSON/CSV/playback, cooperative stopping, and native review/calibration/correction/manual entry.

Synthetic video and mocked poses isolate pipeline behaviour. Qt tests run offscreen. These checks verify arithmetic and program behaviour, not event-wide detection accuracy or physical-height accuracy.

## Real footage

- Original stream metadata: 1920 by 1080, about 29.97 fps, 167044 frames, approximately 5573.7 seconds.
- Latest detailed first-run scan: 45 seconds, 270 samples at 6 per second, 6 candidates, 223 sampled image gaps, no recorded decode errors. Runtime about 47.1 seconds. The first-run spectator case was reproduced and a magnified moving crop recovered the airborne rider.
- Latest whole-event scan: 11148 samples at 2 per second across 5573.7 seconds, 7084 sampled image gaps, 288 unreviewed candidates in 79 heuristic riding sequences. 158 intervals were skipped by takeoff/quality rules and saved in skipped.csv. 54 candidates have single-frame support. Recorded decode errors: 0. Processing runtime: 1608.2 seconds.
- Whole-event samples were regrouped with the final takeoff and peak-quality checks; their snapshots, report, CSV, and skipped-interval CSV were regenerated from those stored detections. The pose/motion detector is the same revision throughout that pass.
- The fast first-run samples and the detailed first-run scan both retained six candidate groups. This is a local sanity check, not a labelled evaluation of the whole event.
- Original direct-link reading was tested at full resolution over seconds 9 through 12. An earlier app build also completed a 12-second real-video window test at 6 samples per second.
- The final packaged Windows app completed a 45-second real-video scan through its actual window: 90 samples at 2 per second, 6 candidates, no recorded errors. It saved both jumps.csv and skipped.csv. The native white layout, hidden scan settings, run columns, SVG icons, and metre-reference controls were inspected in the actual window.

Whole-event and detailed tests use a 960 by 540, 6-fps local proxy. Sampling can miss brief jumps and the exact apex. Processing the entire recording does not prove that every athlete or every jump was detected. Riding-sequence numbers do not identify athlete names or remove replays. Some reviewed contact images still showed wrong lip choices or people, so all automatic candidates remain unreviewed.

The earlier detector's complete scan is retained separately as Earlier full scan. It has 291 unreviewed candidates and is not the current result. Event media and personal session files are excluded from the public source repository.

## Windows build fix

The first executable failed while importing QtCore because dependency collection had selected an incompatible Poppler ICU DLL from another tool's PATH. The build now restricts dependency search to Windows system directories during collection. The packaged app opens through Lip.exe without that unrelated DLL. Its model and required runtime are bundled.

## Remaining validation

There is no labelled ground truth for this recording. Precision, recall, athlete identity accuracy, peak timing error, and physical height error have not been measured. Candidate counts and measured-frame coverage are not accuracy percentages.

The supplied 6.7 m height, 160 m length, 22 m width, 18-degree slope, and 81-degree wall inclination are recorded. They have not been matched to surveyed image correspondences or camera parameters. No real-event metre values have been filled in. Known-reference metre arithmetic passes its tests; physical event heights still require appropriate calibration.
