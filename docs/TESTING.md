# Testing record

Date: 2026-10-12. Computer: Windows 11, Python 3.12.14, CPU inference. Dependency versions are pinned in requirements.txt.

## Automated checks

`python -m unittest -v`: 27 checks passed.

Checks cover horizontal/sloped/reversed lip points, signed gaps, invalid points and scales, upright/tilted known metre references, invalid reference lengths/directions, positive-sample grouping, scene cuts, missing evidence, isolated peak spikes, motion ranking that releases a spectator, local blue boundary fitting, range limits, saved JSON/CSV/review playback, stopping with partial results, and native review/correction/manual-entry actions.

The session tests use a synthetic clip and a mocked pose detector to isolate the pipeline. The window tests run Qt offscreen. These tests verify program behaviour and arithmetic, not detection or physical-height accuracy on unseen events.

## Real footage checks

- Original stream metadata: 1920 by 1080, about 29.97 frames per second, 167044 frames, about 5573.7 seconds.
- Latest detector: first 45-second proxy run, 270 samples at 6 per second, 6 candidate groups. It completed with JSON, CSV, peak images, and readable marked playback. Visual checks included the airborne athlete where the earlier detector had selected a spectator. Some hip and lip marks remain weak or ambiguous.
- Direct original URL: seconds 9 through 12, 2 samples per second. Completed with 6 full-resolution samples and one candidate. This checks direct-link reading as well as local-file reading.
- Packaged Windows app: a 12-second real-video range was started through the actual window. It completed with 72 samples and one candidate, saved under LOCALAPPDATA/Lip/sessions. This checks the bundled model and runtime in the executable, rather than only the Python environment.
- Earlier whole-event scan: 11148 samples at 2 per second, 6977 samples with an image gap, 291 unreviewed candidate groups, no recorded decode errors, completed in about 965 seconds. This scan predates the final motion/crop and peak-selection revision. Its results are retained locally and explicitly labelled earlier.

The full-event test used a 960 by 540, 6-frame-per-second proxy. The final detector was not rerun over all 93 minutes during this session. No event footage or private session is included in the public source repository.

## Packaging fix

The first executable failed importing QtCore. Dependency collection had selected Poppler's ICU DLL from an unrelated tool's PATH. The final build restricts dependency search to Windows system directories during collection. Lip then opened successfully through its normal executable. The package contains no Poppler ICU replacement. The UI was inspected in the actual Windows window.

## What remains unvalidated

No labelled ground-truth dataset was available. Precision, recall, peak timing error, and physical height error have not been measured. Metre arithmetic is tested with known geometry, but no confirmed local physical reference exists for the supplied recording. Candidate counts and evidence coverage must not be presented as accuracy. Automatic results require review. Camera calibration is still needed for reliable physical measurement.

