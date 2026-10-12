"""Find people, estimate hips, and fit a local blue lip in a video image."""

import hashlib
import os
from pathlib import Path
from urllib.request import urlopen

import cv2
import numpy as np
import onnxruntime as ort

MODEL_URL = 'https://huggingface.co/Xenova/yolov8n-pose/resolve/main/onnx/model.onnx'
MODEL_SHA256 = '04f6d2416266f2aba6c5ba8b26de33ed9eba3279f972ac02e33f9f1366547586'


def data_folder():
    """Keep downloaded models and sessions in one user-writable folder."""
    folder = Path(os.getenv('LOCALAPPDATA', str(Path.home() / '.cache'))) / 'Lip'
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def ensure_model(progress=lambda text: None, cancelled=lambda: False):
    """Use bundled weights or download the exact verified model once."""
    bundled = Path(__file__).parent / 'models' / 'pose.onnx'
    target = bundled if bundled.exists() else data_folder() / 'pose.onnx'
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == MODEL_SHA256:
        return target
    temporary = target.with_suffix('.download')
    progress('Downloading the pose model. This only happens once.')
    with urlopen(MODEL_URL, timeout=30) as response, open(temporary, 'wb') as output:
        while chunk := response.read(262144):
            if cancelled():
                raise InterruptedError('Model download stopped.')
            output.write(chunk)
    if hashlib.sha256(temporary.read_bytes()).hexdigest() != MODEL_SHA256:
        raise ValueError('The model download failed its checksum. Please try again.')
    temporary.replace(target)
    return target


class PoseDetector:
    """Run a small pretrained pose model locally on the CPU."""

    def __init__(self, path):
        options = ort.SessionOptions()
        options.intra_op_num_threads = min(4, os.cpu_count() or 1)
        self.session = ort.InferenceSession(str(path), sess_options=options, providers=['CPUExecutionProvider'])
        self.input_name = self.session.get_inputs()[0].name

    def detect(self, frame, threshold=0.28, motion=None):
        """Search the full image and magnified moving regions, including rotated poses."""
        people = self.detect_upright(frame, threshold)
        height, width = frame.shape[:2]
        regions = motion_regions(motion, frame.shape) if motion else []
        left, top = round(width * 0.2), round(height * 0.05)
        crop = frame[top:round(height * 0.95), left:round(width * 0.8)]
        for person in self.detect_upright(crop, threshold) if not regions and motion is None else []:
            person['box'][0] += left
            person['box'][1] += top
            person['hip'] = [person['hip'][0] + left, person['hip'][1] + top]
            person['points'] = [[point[0] + left, point[1] + top, point[2]] for point in person['points']]
            people.append(person)
        for left, top, right, bottom in regions:
            region = frame[top:bottom, left:right]
            region_height, region_width = region.shape[:2]
            for turn in (0, 1, 2, 3):
                for person in self.detect_upright(np.rot90(region, turn).copy(), threshold):
                    self.restore_person(person, turn, region_width, region_height, left, top)
                    people.append(person)
        if not regions and motion is None:
            for turn in (1, 3):
                for person in self.detect_upright(np.rot90(frame, turn).copy(), threshold):
                    self.restore_person(person, turn, width, height)
                    people.append(person)
        keep = cv2.dnn.NMSBoxes([person['box'] for person in people], [person['score'] for person in people], threshold, 0.45)
        return [people[index] for index in np.asarray(keep).reshape(-1)]

    @staticmethod
    def restore_person(person, turn, width, height, left=0, top=0):
        """Undo a crop rotation for every box corner and body landmark."""
        def restore(point):
            x, y = point[:2]
            if turn == 1:
                x, y = width - 1 - y, x
            elif turn == 2:
                x, y = width - 1 - x, height - 1 - y
            elif turn == 3:
                x, y = y, height - 1 - x
            return [float(x + left), float(y + top)]
        x, y, w, h = person['box']
        corners = np.array([restore([x, y]), restore([x + w, y + h])])
        minimum, maximum = corners.min(axis=0), corners.max(axis=0)
        person['box'] = [*minimum.tolist(), *(maximum - minimum).tolist()]
        person['hip'] = restore(person['hip'])
        person['points'] = [restore(point) + [point[2]] for point in person['points']]

    def detect_upright(self, frame, threshold=0.28):
        """Return person boxes and 17 body landmarks in original image pixels."""
        height, width = frame.shape[:2]
        ratio = min(640 / width, 640 / height)
        resized = cv2.resize(frame, (round(width * ratio), round(height * ratio)))
        left = (640 - resized.shape[1]) // 2
        top = (640 - resized.shape[0]) // 2
        padded = np.full((640, 640, 3), 114, dtype=np.uint8)
        padded[top:top + resized.shape[0], left:left + resized.shape[1]] = resized
        tensor = padded[:, :, ::-1].transpose(2, 0, 1)[None].astype(np.float32) / 255.0
        predictions = self.session.run(None, {self.input_name: tensor})[0][0].T
        predictions = predictions[predictions[:, 4] >= threshold]
        boxes, scores, poses = [], [], []
        for prediction in predictions:
            cx, cy, box_width, box_height = prediction[:4]
            box = [(cx - box_width / 2 - left) / ratio, (cy - box_height / 2 - top) / ratio, box_width / ratio, box_height / ratio]
            points = prediction[5:].reshape(17, 3).copy()
            points[:, 0] = (points[:, 0] - left) / ratio
            points[:, 1] = (points[:, 1] - top) / ratio
            if box[2] < 12 or box[3] < 16:
                continue
            boxes.append(list(map(float, box)))
            scores.append(float(prediction[4]))
            poses.append(points)
        keep = cv2.dnn.NMSBoxes(boxes, scores, threshold, 0.45)
        people = []
        for index in np.asarray(keep).reshape(-1):
            points = poses[index]
            hips = points[[11, 12]]
            visible = hips[:, 2] >= 0.30
            if not visible.any():
                continue
            hip = np.average(hips[visible, :2], axis=0, weights=hips[visible, 2])
            if not (0 <= hip[0] < width and 0 <= hip[1] < height):
                continue
            people.append(dict(box=boxes[index], hip=hip.tolist(), score=scores[index], hip_score=float(hips[visible, 2].mean()), points=points.tolist()))
        return people


def choose_athlete(people, frame_shape, previous=None):
    """Prefer a central prominent person, then favour continuity across frames."""
    if not people:
        return None
    height, width = frame_shape[:2]
    ranked = []
    for person in people:
        x, y, box_width, box_height = person['box']
        central = 1 - min(1, abs(person['hip'][0] / width - 0.5) * 1.5)
        prominence = min(1, box_width * box_height / (width * height) * 12)
        rank = person['score'] * 0.20 + central * 0.30 + prominence * 0.15 + person.get('motion', 0) * 0.65
        if previous is not None:
            distance = np.linalg.norm((np.array(person['hip']) - previous['hip']) / [width, height])
            rank += max(0, 0.25 - distance)
        ranked.append((rank, person))
    ranked.sort(key=lambda item: item[0], reverse=True)
    best = dict(ranked[0][1])
    best['ambiguous'] = bool(len(ranked) > 1 and ranked[0][0] - ranked[1][0] < 0.10)
    return best


def motion_field(previous_frame, frame):
    """Remove camera pan and zoom from tracked feature movement."""
    if previous_frame is None or previous_frame.shape != frame.shape:
        return None
    ratio = min(1, 640 / frame.shape[1])
    size = (round(frame.shape[1] * ratio), round(frame.shape[0] * ratio))
    before = cv2.resize(cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY), size)
    after = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), size)
    points = cv2.goodFeaturesToTrack(before, 800, 0.01, 5)
    if points is None or len(points) < 12:
        return None
    moved, status, errors = cv2.calcOpticalFlowPyrLK(before, after, points, None)
    if moved is None:
        return None
    valid = status.reshape(-1) == 1
    old, new = points.reshape(-1, 2)[valid], moved.reshape(-1, 2)[valid]
    if len(old) < 12:
        return None
    transform, inliers = cv2.estimateAffinePartial2D(old, new, method=cv2.RANSAC, ransacReprojThreshold=3)
    if transform is None:
        return None
    predicted = old @ transform[:, :2].T + transform[:, 2]
    residual = np.linalg.norm(new - predicted, axis=1)
    baseline = float(np.median(residual))
    return dict(points=new, residual=residual, baseline=baseline, ratio=ratio, size=size)


def motion_regions(field, frame_shape):
    """Magnify the strongest moving cluster so a small airborne rider can be found."""
    width, height = field['size']
    points, residual = field['points'], field['residual']
    moving = residual > max(3, field['baseline'] * 3)
    mask = np.zeros((height, width), dtype=np.uint8)
    for point in points[moving]:
        cv2.circle(mask, tuple(np.rint(point).astype(int)), 12, 255, -1)
    count, labels, stats, centres = cv2.connectedComponentsWithStats(mask)
    ranked = []
    for x, y, w, h, area in stats[1:]:
        inside = moving & (points[:, 0] >= x) & (points[:, 0] <= x + w) & (points[:, 1] >= y) & (points[:, 1] <= y + h)
        if inside.sum() < 5 or w * h > width * height * 0.4:
            continue
        centre = points[inside].mean(axis=0) / field['ratio']
        if not frame_shape[1] * 0.15 < centre[0] < frame_shape[1] * 0.85:
            continue
        side = max(200 * frame_shape[1] / 960, max(w, h) / field['ratio'] * 1.1)
        left, top = np.maximum([0, 0], centre - side / 2).astype(int)
        right, bottom = np.minimum([frame_shape[1], frame_shape[0]], centre + side / 2).astype(int)
        ranked.append((float(residual[inside].sum()), [left, top, right, bottom]))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in ranked[:1]]


def score_motion(previous_frame, frame, people, field=None):
    """Score each person against the same camera compensated feature field."""
    field = field if field is not None else motion_field(previous_frame, frame)
    if field is None:
        return
    new, residual, baseline = field['points'], field['residual'], field['baseline']
    for person in people:
        x, y, w, h = np.array(person['box']) * field['ratio']
        inside = (new[:, 0] >= x) & (new[:, 0] <= x + w) & (new[:, 1] >= y) & (new[:, 1] <= y + h)
        if inside.sum() >= 3:
            motion = max(0, float(np.percentile(residual[inside], 70)) - baseline)
            person['motion'] = min(1, motion / max(2, field['size'][1] * 0.025))


def find_lip(frame, hip, box):
    """Fit the top local blue boundary and reject sparse or unstable fits."""
    height, width = frame.shape[:2]
    small = cv2.resize(frame, (min(960, width), round(height * min(960, width) / width)))
    ratio = small.shape[1] / width
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (80, 35, 60), (118, 255, 255))
    count, labels, stats, centres = cv2.connectedComponentsWithStats(mask)
    clean = np.zeros_like(mask)
    for component in range(1, count):
        x, y, w, h, area = stats[component]
        if w >= 15 and area >= 25:
            clean[labels == component] = 255
    hip_x, hip_y = np.array(hip) * ratio
    radius = max(65, min(240, box[2] * ratio * 1.8))
    first = max(0, int(hip_x - radius))
    last = min(small.shape[1], int(hip_x + radius))
    xs, ys = [], []
    for x in range(first, last, 2):
        pixels = np.flatnonzero(clean[:, x])
        if len(pixels):
            xs.append(x)
            ys.append(float(pixels[0]))
    if len(xs) < 12:
        return None
    xs, ys = np.array(xs, dtype=float), np.array(ys, dtype=float)
    best = None
    rng = np.random.default_rng(7)
    for _ in range(80):
        pair = rng.choice(len(xs), 2, replace=False)
        if abs(xs[pair[1]] - xs[pair[0]]) < radius * 0.35:
            continue
        slope = (ys[pair[1]] - ys[pair[0]]) / (xs[pair[1]] - xs[pair[0]])
        intercept = ys[pair[0]] - slope * xs[pair[0]]
        errors = np.abs(ys - (slope * xs + intercept))
        inliers = errors < max(5, small.shape[0] * 0.012)
        support = int(inliers.sum())
        if best is None or support > best[0]:
            best = (support, inliers)
    if best is None or best[0] < 10:
        return None
    selected_x, selected_y = xs[best[1]], ys[best[1]]
    if np.ptp(selected_x) < radius * 0.45:
        return None
    slope, intercept = np.polyfit(selected_x, selected_y, 1)
    residual = float(np.median(np.abs(selected_y - (slope * selected_x + intercept))))
    lip_y = float((slope * hip_x + intercept) / ratio)
    extrapolation = max(selected_x.min() - hip_x, hip_x - selected_x.max(), 0)
    if extrapolation > radius * 0.65 or not 0 <= lip_y < height:
        return None
    confidence = min(1, best[0] / max(12, len(xs)) * (1 - min(0.8, residual / 12)))
    if extrapolation > 0:
        confidence *= 0.65
    a = [float(selected_x.min() / ratio), float((slope * selected_x.min() + intercept) / ratio)]
    b = [float(selected_x.max() / ratio), float((slope * selected_x.max() + intercept) / ratio)]
    return dict(a=a, b=b, y=lip_y, score=confidence, extrapolated=bool(extrapolation > 0))


def annotate(frame, sample):
    """Draw the evidence for one measurement, with colours matching the app."""
    output = frame.copy()
    person = sample.get('person')
    lip = sample.get('lip')
    if person:
        x, y, w, h = map(round, person['box'])
        cv2.rectangle(output, (x, y), (x + w, y + h), (110, 225, 190), 2)
        points = person['points']
        for a, b in [(5, 6), (5, 11), (6, 12), (11, 12), (11, 13), (12, 14), (13, 15), (14, 16)]:
            if min(points[a][2], points[b][2]) > 0.3:
                cv2.line(output, tuple(map(round, points[a][:2])), tuple(map(round, points[b][:2])), (110, 225, 190), 2)
        hip = tuple(map(round, person['hip']))
        cv2.circle(output, hip, 6, (80, 225, 255), -1)
        if lip:
            cv2.line(output, tuple(map(round, lip['a'])), tuple(map(round, lip['b'])), (255, 185, 60), 3)
            cv2.line(output, hip, (hip[0], round(lip['y'])), (80, 225, 255), 2)
    label = sample.get('status', 'Review')
    if sample.get('height_px') is not None:
        label = f"Hip above local lip: {sample['height_px']:.1f} px | Review required"
    cv2.rectangle(output, (12, 12), (min(output.shape[1] - 12, 760), 56), (26, 31, 40), -1)
    cv2.putText(output, label, (24, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (240, 240, 240), 2)
    return output
