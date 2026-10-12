"""Measure an image-space vertical gap from two lip points and a hip point."""

import math


def measure_height(lip_a, lip_b, hip, pixels_per_metre=None):
    """Return signed original-image pixels and an optional rough metre estimate."""
    x1, y1 = lip_a
    x2, y2 = lip_b
    hip_x, hip_y = hip
    values = (x1, y1, x2, y2, hip_x, hip_y)
    if not all(math.isfinite(value) for value in values):
        raise ValueError('All point coordinates must be finite numbers.')
    if abs(x2 - x1) < 5:
        raise ValueError('Choose lip points at least 5 pixels apart horizontally.')
    if not min(x1, x2) <= hip_x <= max(x1, x2):
        raise ValueError('The two lip points must bracket the hip horizontally.')
    lip_y = y1 + (y2 - y1) * (hip_x - x1) / (x2 - x1)
    height_px = lip_y - hip_y
    height_m = None
    if pixels_per_metre is not None:
        if not math.isfinite(pixels_per_metre) or pixels_per_metre <= 0:
            raise ValueError('Pixels per metre must be a finite number above zero.')
        height_m = height_px / pixels_per_metre
    return height_px, height_m, lip_y


def calibrate_height(lip_a, lip_b, hip, reference_top, reference_bottom, reference_metres):
    """Estimate height using a known local vertical reference in the same image."""
    values = [*lip_a, *lip_b, *hip, *reference_top, *reference_bottom, reference_metres]
    if not all(math.isfinite(value) for value in values) or reference_metres <= 0:
        raise ValueError('Use finite coordinates and a known reference length above zero.')
    dx = reference_bottom[0] - reference_top[0]
    dy = reference_bottom[1] - reference_top[1]
    length = math.hypot(dx, dy)
    if length < 10 or dy <= 0:
        raise ValueError('Click the top then bottom of a vertical reference at least 10 pixels long.')
    direction = (dx / length, dy / length)
    line = (lip_b[0] - lip_a[0], lip_b[1] - lip_a[1])
    determinant = direction[0] * line[1] - direction[1] * line[0]
    if abs(determinant) < math.hypot(*line) * 0.1:
        raise ValueError('The vertical reference must cross the lip direction clearly.')
    offset = (lip_a[0] - hip[0], lip_a[1] - hip[1])
    gap = (offset[0] * line[1] - offset[1] * line[0]) / determinant
    fraction = (offset[0] * direction[1] - offset[1] * direction[0]) / determinant
    if not 0 <= fraction <= 1:
        raise ValueError('The lip points must bracket the calibrated vertical through the hip.')
    scale = length / reference_metres
    return gap / scale, scale, gap
