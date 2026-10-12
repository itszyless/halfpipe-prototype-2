"""Analyse a whole video in the background and save reviewable jump candidates."""

import csv
import json
import math
import time
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np

from vision import PoseDetector, annotate, choose_athlete, data_folder, ensure_model, find_lip, score_motion


def open_video(source):
    """Open a local file or direct link with bounded network waits."""
    options = [cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 15000, cv2.CAP_PROP_READ_TIMEOUT_MSEC, 10000]
    capture = cv2.VideoCapture(source, cv2.CAP_FFMPEG, options)
    fps = capture.get(cv2.CAP_PROP_FPS)
    count = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    if not capture.isOpened() or not math.isfinite(fps) or fps <= 0 or not math.isfinite(count) or count < 1:
        capture.release()
        raise ValueError('Cannot read this video. Try a local MP4 file or a direct video link.')
    return capture, fps, int(count)


def find_jumps(samples, sample_rate):
    """Group positive above-lip samples, bridge short gaps, and choose robust peaks."""
    groups, active = [], []
    gap_limit = max(0.55, 2.1 / sample_rate)
    for index, sample in enumerate(samples):
        gap = sample.get('height_px')
        person = sample.get('person')
        positive = person is not None and gap is not None and gap > max(8, person['box'][3] * 0.12)
        if active and (sample['time'] - samples[active[-1]]['time'] > gap_limit or sample.get('cut')):
            groups.append(active)
            active = []
        if positive:
            active.append(index)
    if active:
        groups.append(active)
    jumps = []
    for group in groups:
        if len(group) < 2:
            continue
        values = np.array([samples[index]['height_px'] for index in group])
        smoothed = np.array([np.median(values[max(0, i - 1):i + 2]) for i in range(len(values))])
        near_peak = np.flatnonzero(smoothed >= smoothed.max() * 0.95)
        chosen = int(min(near_peak, key=lambda i: abs(values[i] - smoothed[i])))
        peak = samples[group[chosen]]
        start, end = samples[group[0]]['time'], samples[group[-1]]['time']
        reasons = ['Camera scale and vertical direction are not calibrated.']
        if end - start > 8:
            reasons.append('Long above-lip segment; possible spectator or wrong line.')
        if any(samples[index]['person'].get('ambiguous') for index in group):
            reasons.append('More than one person could be the athlete.')
        if peak['lip']['extrapolated']:
            reasons.append('Lip was extended beyond its visible support.')
        if peak['confidence'] < 0.55:
            reasons.append('Weak hip or lip evidence at the peak.')
        if group[0] == 0 or group[-1] == len(samples) - 1:
            reasons.append('Candidate touches an analysis boundary.')
        jumps.append(dict(id=len(jumps) + 1, start=round(start, 3), end=round(end, 3), peak_time=peak['time'], frame=peak['frame'], height_px=round(peak['height_px'], 2), height_m=None, confidence=round(peak['confidence'], 3), reviewed=False, excluded=False, reasons=reasons, sample_index=group[chosen], scale=None))
    return jumps


def save_report(report, folder):
    """Atomically save the session so partial runs can still be inspected."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    temporary = folder / 'report.tmp'
    temporary.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    temporary.replace(folder / 'report.json')


def export_csv(report, path):
    """Export accepted and excluded candidates with their review status."""
    columns = ['jump', 'start_seconds', 'end_seconds', 'peak_seconds', 'frame', 'height_px', 'estimated_height_m', 'pixels_per_metre', 'confidence', 'reviewed', 'excluded', 'notes', 'calibration']
    with open(path, 'w', newline='', encoding='utf-8-sig') as output:
        writer = csv.writer(output)
        writer.writerow(columns)
        for jump in report['jumps']:
            writer.writerow([jump['id'], jump['start'], jump['end'], jump['peak_time'], jump['frame'], jump['height_px'], '' if jump['height_m'] is None else jump['height_m'], '' if jump['scale'] is None else jump['scale'], jump['confidence'], jump['reviewed'], jump['excluded'], ' '.join(jump['reasons']), json.dumps(jump.get('calibration'))])


def analyse(source, start=0, end=0, sample_rate=6, progress=lambda data: None, preview=lambda frame: None, cancelled=lambda: False, folder=None, model_path=None):
    """Sample the requested range without holding the whole movie in memory."""
    source = str(source)
    if not source.startswith(('https://', 'http://')):
        source = str(Path(source).expanduser().resolve())
    if not 1 <= sample_rate <= 30 or not math.isfinite(start) or not math.isfinite(end) or start < 0 or end < 0:
        raise ValueError('Use 1 to 30 samples per second and nonnegative start/end times.')
    model_path = model_path or ensure_model(lambda text: progress(dict(message=text, percent=0)), cancelled)
    detector = PoseDetector(model_path)
    capture, fps, count = open_video(source)
    duration = count / fps
    end = min(end, duration) if end else duration
    if start >= end:
        capture.release()
        raise ValueError('The start time must be before the end of the selected range.')
    folder = Path(folder) if folder else data_folder() / 'sessions' / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    folder.mkdir(parents=True, exist_ok=True)
    report = dict(version=2, source=source, fps=fps, frame_count=count, width=0, height=0, start=start, end=end, sample_rate=sample_rate, state='running', complete=False, next_frame=round(start * fps), samples=[], jumps=[], errors=[], folder=str(folder), model_sha256='04f6d2416266f2aba6c5ba8b26de33ed9eba3279f972ac02e33f9f1366547586')
    first = round(start * fps)
    last = min(count, math.ceil(end * fps))
    stride = max(1, round(fps / sample_rate))
    report['effective_sample_rate'] = fps / stride
    report['detector_revision'] = 'crop-motion-v1'
    capture.set(cv2.CAP_PROP_POS_FRAMES, first)
    previous, previous_image, previous_frame = None, None, None
    started = time.monotonic()
    index, failures, measured = first, 0, 0
    writer = None
    try:
        while index < last and not cancelled():
            ok, frame = capture.read()
            if not ok:
                failures += 1
                report['errors'].append(f'Could not decode frame {index}.')
                if failures >= 3:
                    report['state'] = 'read_error'
                    break
                index += stride
                capture.set(cv2.CAP_PROP_POS_FRAMES, index)
                continue
            failures = 0
            report['height'], report['width'] = frame.shape[:2]
            if writer is None:
                ratio = min(1, 960 / frame.shape[1])
                review_size = (int(frame.shape[1] * ratio) // 2 * 2, int(frame.shape[0] * ratio) // 2 * 2)
                writer = cv2.VideoWriter(str(folder / 'review.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), fps / stride, review_size)
                report['review_video'] = 'review.mp4' if writer.isOpened() else None
                report['review_note'] = 'Sampled, silent review video. Frame timestamps refer to the source. Later point corrections appear in snapshots and CSV only.'
            tiny = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (64, 36)).astype(float)
            cut = previous_image is not None and np.abs(tiny - previous_image).mean() > 45
            if cut:
                previous = None
            people = detector.detect(frame)
            if not cut:
                score_motion(previous_frame, frame, people)
            person = choose_athlete(people, frame.shape, previous)
            lip = find_lip(frame, person['hip'], person['box']) if person else None
            height_px = lip['y'] - person['hip'][1] if lip else None
            confidence = min(person['score'], person['hip_score'], lip['score']) if lip else 0
            if lip and abs(height_px) > frame.shape[0] * 0.8:
                height_px = None
                confidence = 0
            status = 'Measured image gap' if height_px is not None else ('Lip not clear' if person else 'Athlete not found')
            sample = dict(frame=index, time=round(index / fps, 3), person=person, lip=lip, height_px=height_px, confidence=float(confidence), status=status, cut=bool(cut))
            report['samples'].append(sample)
            measured += height_px is not None
            marked = annotate(frame, sample)
            cv2.putText(marked, f'Source {index / fps:.2f}s', (24, frame.shape[0] - 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            if writer.isOpened():
                writer.write(cv2.resize(marked, review_size))
            previous, previous_image = person, tiny
            previous_frame = frame
            report['next_frame'] = min(last, index + stride)
            percent = (index - first + 1) / max(1, last - first) * 100
            elapsed = time.monotonic() - started
            remaining = elapsed * (100 - percent) / max(0.01, percent)
            if len(report['samples']) % 3 == 1:
                preview(marked)
                progress(dict(percent=percent, time=sample['time'], samples=len(report['samples']), measured=measured, remaining=remaining, message=f"Analysing {sample['time']:.1f} seconds"))
            if len(report['samples']) % 500 == 0:
                report['jumps'] = find_jumps(report['samples'], sample_rate)
                save_report(report, folder)
            for _ in range(min(stride - 1, last - index - 1)):
                if cancelled():
                    break
                capture.grab()
            index += stride
        if cancelled():
            report['state'] = 'stopped'
        elif report['state'] == 'running':
            report['state'] = 'complete'
            report['complete'] = True
        report['jumps'] = find_jumps(report['samples'], sample_rate)
        report['elapsed_seconds'] = round(time.monotonic() - started, 2)
        for jump in report['jumps']:
            if cancelled():
                break
            capture.set(cv2.CAP_PROP_POS_FRAMES, jump['frame'])
            ok, frame = capture.read()
            if ok:
                filename = f"jump-{jump['id']:03}.jpg"
                cv2.imwrite(str(folder / filename), annotate(frame, report['samples'][jump['sample_index']]))
                jump['snapshot'] = filename
        save_report(report, folder)
        export_csv(report, folder / 'jumps.csv')
        return report
    except Exception as error:
        report['state'] = 'error'
        report['errors'].append(str(error))
        report['jumps'] = find_jumps(report['samples'], sample_rate)
        save_report(report, folder)
        raise
    finally:
        capture.release()
        if writer is not None:
            writer.release()
