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
