# Every Python source line explained

Read BEGINNER_GUIDE.md first for a gentle introduction and worked numbers. This document covers every line of the eight Python files shipped in this version, including blank lines and styles. Build commands are explained separately in BUILD_GUIDE.md. The licence texts are external notices, not application code.

Each entry shows the exact source line and its meaning. Long statements do several things, so their explanation lists the arguments and fields. A dot means an attribute or method of an object. Square brackets mean indexing or slicing. Parentheses call a function. Indentation tells you which block owns the line. Definitions prepare code for later; signal connections decide when the window calls it. Values named `self.something` belong to the current object.

For model arrays, shape is the number of entries along each axis. NumPy arithmetic often works on every element at once. For Qt controls, a constructor creates a control, `set...` configures it, `add...` places it, and `.connect(...)` links an event to a function. The beginner guide explains the whole pipeline so the individual operations have context.

## measurement.py

Source SHA-256: `971961664443a0f10c3b625202b72004885fd555d39b97bc3df3306bd55671a8`

### Line 1

```python
"""Measure an image-space vertical gap from two lip points and a hip point."""
```

Documentation string: Measure an image-space vertical gap from two lip points and a hip point. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 2

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 3

```python
import math
```

Import modules: math. Their functions become available through those module names.

### Line 4

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 5

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 6

```python
def measure_height(lip_a, lip_b, hip, pixels_per_metre=None):
```

Define `measure_height(lip_a, lip_b, hip, pixels_per_metre=None)`. Its job: Return signed original-image pixels and an optional rough metre estimate. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 7

```python
    """Return signed original-image pixels and an optional rough metre estimate."""
```

Inside `measure_height`: Documentation string: Return signed original-image pixels and an optional rough metre estimate. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 8

```python
    x1, y1 = lip_a
```

Inside `measure_height`: Store the result in `(x1, y1)`: `lip_a`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 9

```python
    x2, y2 = lip_b
```

Inside `measure_height`: Store the result in `(x2, y2)`: `lip_b`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 10

```python
    hip_x, hip_y = hip
```

Inside `measure_height`: Store the result in `(hip_x, hip_y)`: `hip`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 11

```python
    values = (x1, y1, x2, y2, hip_x, hip_y)
```

Inside `measure_height`: Store the result in `values`: tuple containing `x1`; `y1`; `x2`; `y2`; `hip_x`; `hip_y`. This is assignment, not an equality check.

### Line 12

```python
    if not all(math.isfinite(value) for value in values):
```

Inside `measure_height`: Run the indented block only when this condition is true: NOT `all`: check whether every supplied condition is true. Arguments: produce `math.isfinite`: check that a number is neither infinite nor NaN. Arguments: `value`, for each value in `values`. Other branches handle the remaining case.

### Line 13

```python
        raise ValueError('All point coordinates must be finite numbers.')
```

Inside `measure_height`: Stop this operation by raising an exception: `ValueError`: call this function with the supplied arguments. Arguments: `'All point coordinates must be finite numbers.'`. A matching except block can handle it.

### Line 14

```python
    if abs(x2 - x1) < 5:
```

Inside `measure_height`: Run the indented block only when this condition is true: `abs`: call this function with the supplied arguments. Arguments: (`x2` minus `x1`) is less than `5`. Other branches handle the remaining case.

### Line 15

```python
        raise ValueError('Choose lip points at least 5 pixels apart horizontally.')
```

Inside `measure_height`: Stop this operation by raising an exception: `ValueError`: call this function with the supplied arguments. Arguments: `'Choose lip points at least 5 pixels apart horizontally.'`. A matching except block can handle it.

### Line 16

```python
    if not min(x1, x2) <= hip_x <= max(x1, x2):
```

Inside `measure_height`: Run the indented block only when this condition is true: NOT `min`: choose the smallest value, or the item with the smallest key. Arguments: `x1`; `x2` is at most `hip_x` and is at most `max`: choose the largest value, or the item with the largest key. Arguments: `x1`; `x2`. Other branches handle the remaining case.

### Line 17

```python
        raise ValueError('The two lip points must bracket the hip horizontally.')
```

Inside `measure_height`: Stop this operation by raising an exception: `ValueError`: call this function with the supplied arguments. Arguments: `'The two lip points must bracket the hip horizontally.'`. A matching except block can handle it.

### Line 18

```python
    lip_y = y1 + (y2 - y1) * (hip_x - x1) / (x2 - x1)
```

Inside `measure_height`: Linearly interpolate the lip at the hip X. `(hip_x - x1) / (x2 - x1)` is the horizontal fraction along the segment. Multiply the segment's Y change by that fraction and add the starting Y. Earlier checks prevent a zero denominator and reject a hip outside the segment.

### Line 19

```python
    height_px = lip_y - hip_y
```

Inside `measure_height`: Subtract the hip Y from the interpolated lip Y. Image Y increases downward, so a hip higher in the picture has a smaller Y and produces a positive gap. This is image-space height only.

### Line 20

```python
    height_m = None
```

Inside `measure_height`: Store the result in `height_m`: `None`. This is assignment, not an equality check.

### Line 21

```python
    if pixels_per_metre is not None:
```

Inside `measure_height`: Run the indented block only when this condition is true: `pixels_per_metre` is not the same object as `None`. Other branches handle the remaining case.

### Line 22

```python
        if not math.isfinite(pixels_per_metre) or pixels_per_metre <= 0:
```

Inside `measure_height`: Run the indented block only when this condition is true: NOT `math.isfinite`: check that a number is neither infinite nor NaN. Arguments: `pixels_per_metre` OR `pixels_per_metre` is at most `0`. Other branches handle the remaining case.

### Line 23

```python
            raise ValueError('Pixels per metre must be a finite number above zero.')
```

Inside `measure_height`: Stop this operation by raising an exception: `ValueError`: call this function with the supplied arguments. Arguments: `'Pixels per metre must be a finite number above zero.'`. A matching except block can handle it.

### Line 24

```python
        height_m = height_px / pixels_per_metre
```

Inside `measure_height`: Divide the pixel gap by the explicitly supplied local pixels-per-metre scale. This computes an estimate under the caller's calibration assumptions; it does not establish camera calibration.

### Line 25

```python
    return height_px, height_m, lip_y
```

Inside `measure_height`: End this function now and send back tuple containing `height_px`; `height_m`; `lip_y`. A bare return sends None.

### Line 26

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 27

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 28

```python
def calibrate_height(lip_a, lip_b, hip, reference_top, reference_bottom, reference_metres):
```

Define `calibrate_height(lip_a, lip_b, hip, reference_top, reference_bottom, reference_metres)`. Its job: Estimate height using a known local vertical reference in the same image. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 29

```python
    """Estimate height using a known local vertical reference in the same image."""
```

Inside `calibrate_height`: Documentation string: Estimate height using a known local vertical reference in the same image. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 30

```python
    values = [*lip_a, *lip_b, *hip, *reference_top, *reference_bottom, reference_metres]
```

Inside `calibrate_height`: Store the result in `values`: list containing `*lip_a`; `*lip_b`; `*hip`; `*reference_top`; `*reference_bottom`; `reference_metres`. This is assignment, not an equality check.

### Line 31

```python
    if not all(math.isfinite(value) for value in values) or reference_metres <= 0:
```

Inside `calibrate_height`: Run the indented block only when this condition is true: NOT `all`: check whether every supplied condition is true. Arguments: produce `math.isfinite`: check that a number is neither infinite nor NaN. Arguments: `value`, for each value in `values` OR `reference_metres` is at most `0`. Other branches handle the remaining case.

### Line 32

```python
        raise ValueError('Use finite coordinates and a known reference length above zero.')
```

Inside `calibrate_height`: Stop this operation by raising an exception: `ValueError`: call this function with the supplied arguments. Arguments: `'Use finite coordinates and a known reference length above zero.'`. A matching except block can handle it.

### Line 33

```python
    dx = reference_bottom[0] - reference_top[0]
```

Inside `calibrate_height`: Store the result in `dx`: (`reference_bottom[0]` minus `reference_top[0]`). This is assignment, not an equality check.

### Line 34

```python
    dy = reference_bottom[1] - reference_top[1]
```

Inside `calibrate_height`: Store the result in `dy`: (`reference_bottom[1]` minus `reference_top[1]`). This is assignment, not an equality check.

### Line 35

```python
    length = math.hypot(dx, dy)
```

Inside `calibrate_height`: Store the result in `length`: `math.hypot`: calculate Euclidean vector length from its horizontal and vertical components. Arguments: `dx`; `dy`. This is assignment, not an equality check.

### Line 36

```python
    if length < 10 or dy <= 0:
```

Inside `calibrate_height`: Run the indented block only when this condition is true: `length` is less than `10` OR `dy` is at most `0`. Other branches handle the remaining case.

### Line 37

```python
        raise ValueError('Click the top then bottom of a vertical reference at least 10 pixels long.')
```

Inside `calibrate_height`: Stop this operation by raising an exception: `ValueError`: call this function with the supplied arguments. Arguments: `'Click the top then bottom of a vertical reference at least 10 pixels long.'`. A matching except block can handle it.

### Line 38

```python
    direction = (dx / length, dy / length)
```

Inside `calibrate_height`: Store the result in `direction`: tuple containing (`dx` divided by `length`); (`dy` divided by `length`). This is assignment, not an equality check.

### Line 39

```python
    line = (lip_b[0] - lip_a[0], lip_b[1] - lip_a[1])
```

Inside `calibrate_height`: Store the result in `line`: tuple containing (`lip_b[0]` minus `lip_a[0]`); (`lip_b[1]` minus `lip_a[1]`). This is assignment, not an equality check.

### Line 40

```python
    determinant = direction[0] * line[1] - direction[1] * line[0]
```

Inside `calibrate_height`: Store the result in `determinant`: ((`direction[0]` times `line[1]`) minus (`direction[1]` times `line[0]`)). This is assignment, not an equality check.

### Line 41

```python
    if abs(determinant) < math.hypot(*line) * 0.1:
```

Inside `calibrate_height`: Run the indented block only when this condition is true: `abs`: call this function with the supplied arguments. Arguments: `determinant` is less than (`math.hypot`: calculate Euclidean vector length from its horizontal and vertical components. Arguments: `*line` times `0.1`). Other branches handle the remaining case.

### Line 42

```python
        raise ValueError('The vertical reference must cross the lip direction clearly.')
```

Inside `calibrate_height`: Stop this operation by raising an exception: `ValueError`: call this function with the supplied arguments. Arguments: `'The vertical reference must cross the lip direction clearly.'`. A matching except block can handle it.

### Line 43

```python
    offset = (lip_a[0] - hip[0], lip_a[1] - hip[1])
```

Inside `calibrate_height`: Store the result in `offset`: tuple containing (`lip_a[0]` minus `hip[0]`); (`lip_a[1]` minus `hip[1]`). This is assignment, not an equality check.

### Line 44

```python
    gap = (offset[0] * line[1] - offset[1] * line[0]) / determinant
```

Inside `calibrate_height`: Store the result in `gap`: (((`offset[0]` times `line[1]`) minus (`offset[1]` times `line[0]`)) divided by `determinant`). This is assignment, not an equality check.

### Line 45

```python
    fraction = (offset[0] * direction[1] - offset[1] * direction[0]) / determinant
```

Inside `calibrate_height`: Store the result in `fraction`: (((`offset[0]` times `direction[1]`) minus (`offset[1]` times `direction[0]`)) divided by `determinant`). This is assignment, not an equality check.

### Line 46

```python
    if not 0 <= fraction <= 1:
```

Inside `calibrate_height`: Run the indented block only when this condition is true: NOT `0` is at most `fraction` and is at most `1`. Other branches handle the remaining case.

### Line 47

```python
        raise ValueError('The lip points must bracket the calibrated vertical through the hip.')
```

Inside `calibrate_height`: Stop this operation by raising an exception: `ValueError`: call this function with the supplied arguments. Arguments: `'The lip points must bracket the calibrated vertical through the hip.'`. A matching except block can handle it.

### Line 48

```python
    scale = length / reference_metres
```

Inside `calibrate_height`: Store the result in `scale`: (`length` divided by `reference_metres`). This is assignment, not an equality check.

### Line 49

```python
    return gap / scale, scale, gap
```

Inside `calibrate_height`: End this function now and send back tuple containing (`gap` divided by `scale`); `scale`; `gap`. A bare return sends None.

## analysis.py

Source SHA-256: `7a3be6a2458abadd47d8ce1b0f22ccb414e89d934e60584e1cc7be87a9d48313`

### Line 1

```python
"""Analyse a whole video in the background and save reviewable jump candidates."""
```

Documentation string: Analyse a whole video in the background and save reviewable jump candidates. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 2

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 3

```python
import csv
```

Import modules: csv. Their functions become available through those module names.

### Line 4

```python
import json
```

Import modules: json. Their functions become available through those module names.

### Line 5

```python
import math
```

Import modules: math. Their functions become available through those module names.

### Line 6

```python
import time
```

Import modules: time. Their functions become available through those module names.

### Line 7

```python
from datetime import datetime
```

Import datetime from `datetime`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 8

```python
from pathlib import Path
```

Import Path from `pathlib`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 9

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 10

```python
import cv2
```

Import modules: cv2. Their functions become available through those module names.

### Line 11

```python
import numpy as np
```

Import modules: numpy under the short name np. Their functions become available through those module names.

### Line 12

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 13

```python
from vision import PoseDetector, annotate, choose_athlete, data_folder, ensure_model, find_lip, motion_field, score_motion
```

Import PoseDetector, annotate, choose_athlete, data_folder, ensure_model, find_lip, motion_field, score_motion from `vision`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 14

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 15

```python
PIPE_DIMENSIONS = dict(wall_height_m=6.7, length_m=160, width_m=22, slope_degrees=18, wall_inclination_degrees=81, source='Dimensions supplied by the user; camera correspondence not yet verified.')
```

Store the result in `PIPE_DIMENSIONS`: `dict`: create a dictionary from the named fields. Arguments: wall_height_m = `6.7`; length_m = `160`; width_m = `22`; slope_degrees = `18`; wall_inclination_degrees = `81`; source = `'Dimensions supplied by the user; camera correspondence not yet verified.'`. This is assignment, not an equality check.

### Line 16

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 17

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 18

```python
def open_video(source):
```

Define `open_video(source)`. Its job: Open a local file or direct link with bounded network waits. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 19

```python
    """Open a local file or direct link with bounded network waits."""
```

Inside `open_video`: Documentation string: Open a local file or direct link with bounded network waits. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 20

```python
    options = [cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 15000, cv2.CAP_PROP_READ_TIMEOUT_MSEC, 10000]
```

Inside `open_video`: Store the result in `options`: list containing `cv2.CAP_PROP_OPEN_TIMEOUT_MSEC`; `15000`; `cv2.CAP_PROP_READ_TIMEOUT_MSEC`; `10000`. This is assignment, not an equality check.

### Line 21

```python
    capture = cv2.VideoCapture(source, cv2.CAP_FFMPEG, options)
```

Inside `open_video`: Store the result in `capture`: `cv2.VideoCapture`: create a video reader. Arguments: `source`; `cv2.CAP_FFMPEG`; `options`. This is assignment, not an equality check.

### Line 22

```python
    fps = capture.get(cv2.CAP_PROP_FPS)
```

Inside `open_video`: Store the result in `fps`: `capture.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `cv2.CAP_PROP_FPS`. This is assignment, not an equality check.

### Line 23

```python
    count = capture.get(cv2.CAP_PROP_FRAME_COUNT)
```

Inside `open_video`: Store the result in `count`: `capture.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `cv2.CAP_PROP_FRAME_COUNT`. This is assignment, not an equality check.

### Line 24

```python
    if not capture.isOpened() or not math.isfinite(fps) or fps <= 0 or not math.isfinite(count) or count < 1:
```

Inside `open_video`: Run the indented block only when this condition is true: NOT `capture.isOpened`: check whether the video resource opened successfully. No arguments are supplied OR NOT `math.isfinite`: check that a number is neither infinite nor NaN. Arguments: `fps` OR `fps` is at most `0` OR NOT `math.isfinite`: check that a number is neither infinite nor NaN. Arguments: `count` OR `count` is less than `1`. Other branches handle the remaining case.

### Line 25

```python
        capture.release()
```

Inside `open_video`: Run this operation: `capture.release`: close the video reader or finalize the video writer. No arguments are supplied.

### Line 26

```python
        raise ValueError('Cannot read this video. Try a local MP4 file or a direct video link.')
```

Inside `open_video`: Stop this operation by raising an exception: `ValueError`: call this function with the supplied arguments. Arguments: `'Cannot read this video. Try a local MP4 file or a direct video link.'`. A matching except block can handle it.

### Line 27

```python
    return capture, fps, int(count)
```

Inside `open_video`: End this function now and send back tuple containing `capture`; `fps`; `int`: convert a value to a whole number. Arguments: `count`. A bare return sends None.

### Line 28

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 29

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 30

```python
def find_jumps(samples, sample_rate, rejected=None):
```

Define `find_jumps(samples, sample_rate, rejected=None)`. Its job: Require below-lip takeoff evidence so an initial deck drop is not a jump. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 31

```python
    """Require below-lip takeoff evidence so an initial deck drop is not a jump."""
```

Inside `find_jumps`: Documentation string: Require below-lip takeoff evidence so an initial deck drop is not a jump. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 32

```python
    groups, active = [], []
```

Inside `find_jumps`: Store the result in `(groups, active)`: tuple containing an empty list `[]`; an empty list `[]`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 33

```python
    gap_limit = max(0.55, 2.1 / sample_rate)
```

Inside `find_jumps`: Store the result in `gap_limit`: `max`: choose the largest value, or the item with the largest key. Arguments: `0.55`; (`2.1` divided by `sample_rate`). This is assignment, not an equality check.

### Line 34

```python
    for index, sample in enumerate(samples):
```

Inside `find_jumps`: Repeat the following indented block for each `(index, sample)` from `enumerate`: provide both each item's index and its value. Arguments: `samples`. Tuple targets unpack each loop item.

### Line 35

```python
        gap = sample.get('height_px')
```

Inside `find_jumps`: Store the result in `gap`: `sample.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'height_px'`. This is assignment, not an equality check.

### Line 36

```python
        person = sample.get('person')
```

Inside `find_jumps`: Store the result in `person`: `sample.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'person'`. This is assignment, not an equality check.

### Line 37

```python
        positive = person is not None and gap is not None and gap > max(8, person['box'][3] * 0.12)
```

Inside `find_jumps`: Store the result in `positive`: `person` is not the same object as `None` AND `gap` is not the same object as `None` AND `gap` is greater than `max`: choose the largest value, or the item with the largest key. Arguments: `8`; (`person['box'][3]` times `0.12`). This is assignment, not an equality check.

### Line 38

```python
        below = person is not None and gap is not None and sample.get('confidence', 0) >= 0.25 and gap < -max(8, person['box'][3] * 0.12)
```

Inside `find_jumps`: Store the result in `below`: `person` is not the same object as `None` AND `gap` is not the same object as `None` AND `sample.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'confidence'`; `0` is at least `0.25` AND `gap` is less than negative `max`: choose the largest value, or the item with the largest key. Arguments: `8`; (`person['box'][3]` times `0.12`). This is assignment, not an equality check.

### Line 39

```python
        if active and (sample['time'] - samples[active[-1]]['time'] > gap_limit or sample.get('cut') or below):
```

Inside `find_jumps`: Run the indented block only when this condition is true: `active` AND (`sample['time']` minus `samples[active[-1]]['time']`) is greater than `gap_limit` OR `sample.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'cut'` OR `below`. Other branches handle the remaining case.

### Line 40

```python
            groups.append(active)
```

Inside `find_jumps`: Run this operation: `groups.append`: add an item to the end of this list. Arguments: `active`.

### Line 41

```python
            active = []
```

Inside `find_jumps`: Store the result in `active`: an empty list `[]`. This is assignment, not an equality check.

### Line 42

```python
        if positive:
```

Inside `find_jumps`: Run the indented block only when this condition is true: `positive`. Other branches handle the remaining case.

### Line 43

```python
            active.append(index)
```

Inside `find_jumps`: Run this operation: `active.append`: add an item to the end of this list. Arguments: `index`.

### Line 44

```python
    if active:
```

Inside `find_jumps`: Run the indented block only when this condition is true: `active`. Other branches handle the remaining case.

### Line 45

```python
        groups.append(active)
```

Inside `find_jumps`: Run this operation: `groups.append`: add an item to the end of this list. Arguments: `active`.

### Line 46

```python
    jumps = []
```

Inside `find_jumps`: Store the result in `jumps`: an empty list `[]`. This is assignment, not an equality check.

### Line 47

```python
    for group in groups:
```

Inside `find_jumps`: Repeat the following indented block for each `group` from `groups`. Tuple targets unpack each loop item.

### Line 48

```python
        single = len(group) == 1
```

Inside `find_jumps`: Store the result in `single`: `len`: count items. Arguments: `group` equals `1`. This is assignment, not an equality check.

### Line 49

```python
        if single:
```

Inside `find_jumps`: Run the indented block only when this condition is true: `single`. Other branches handle the remaining case.

### Line 50

```python
            item = samples[group[0]]
```

Inside `find_jumps`: Store the result in `item`: `samples[group[0]]`. This is assignment, not an equality check.

### Line 51

```python
            if sample_rate > 2 or item['confidence'] < 0.25 or item['person'].get('motion', 0) < 0.5 or item['height_px'] < max(20, item['person']['box'][3] * 0.3):
```

Inside `find_jumps`: Run the indented block only when this condition is true: `sample_rate` is greater than `2` OR `item['confidence']` is less than `0.25` OR `item['person'].get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'motion'`; `0` is less than `0.5` OR `item['height_px']` is less than `max`: choose the largest value, or the item with the largest key. Arguments: `20`; (`item['person']['box'][3]` times `0.3`). Other branches handle the remaining case.

### Line 52

```python
                continue
```

Inside `find_jumps`: Skip the rest of this loop iteration and try the next item. This rejects the current unsuitable detection, fit, or sample.

### Line 53

```python
        start, end = samples[group[0]]['time'], samples[group[-1]]['time']
```

Inside `find_jumps`: Store the result in `(start, end)`: tuple containing `samples[group[0]]['time']`; `samples[group[-1]]['time']`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 54

```python
        before = []
```

Inside `find_jumps`: Store the result in `before`: an empty list `[]`. This is assignment, not an equality check.

### Line 55

```python
        for index in range(group[0] - 1, -1, -1):
```

Inside `find_jumps`: Repeat the following indented block for each `index` from `range`: produce integer loop positions, excluding the upper bound. Arguments: (`group[0]` minus `1`); negative `1`; negative `1`. Tuple targets unpack each loop item.

### Line 56

```python
            item = samples[index]
```

Inside `find_jumps`: Store the result in `item`: `samples[index]`. This is assignment, not an equality check.

### Line 57

```python
            if start - item['time'] > 3 or samples[index + 1].get('cut'):
```

Inside `find_jumps`: Run the indented block only when this condition is true: (`start` minus `item['time']`) is greater than `3` OR `samples[index + 1].get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'cut'`. Other branches handle the remaining case.

### Line 58

```python
                break
```

Inside `find_jumps`: End the nearest enclosing loop immediately. Processing continues after the loop.

### Line 59

```python
            if item.get('person') is not None and item.get('height_px') is not None:
```

Inside `find_jumps`: Run the indented block only when this condition is true: `item.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'person'` is not the same object as `None` AND `item.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'height_px'` is not the same object as `None`. Other branches handle the remaining case.

### Line 60

```python
                before.append(item)
```

Inside `find_jumps`: Run this operation: `before.append`: add an item to the end of this list. Arguments: `item`.

### Line 61

```python
        takeoff = any(item.get('confidence', 0) >= 0.20 and item['height_px'] < -max(8, item['person']['box'][3] * 0.12) for item in before)
```

Inside `find_jumps`: Store the result in `takeoff`: `any`: check whether at least one supplied condition is true. Arguments: produce `item.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'confidence'`; `0` is at least `0.2` AND `item['height_px']` is less than negative `max`: choose the largest value, or the item with the largest key. Arguments: `8`; `item['person']['box'][3] * 0.12`, for each item in `before`. This is assignment, not an equality check.

### Line 62

```python
        if not takeoff or end - start > 6:
```

Inside `find_jumps`: Run the indented block only when this condition is true: NOT `takeoff` OR (`end` minus `start`) is greater than `6`. Other branches handle the remaining case.

### Line 63

```python
            if rejected is not None:
```

Inside `find_jumps`: Run the indented block only when this condition is true: `rejected` is not the same object as `None`. Other branches handle the remaining case.

### Line 64

```python
                rejected.append(dict(start=start, end=end, reason='No below-lip takeoff evidence. Possible drop-in or missed tracking.' if not takeoff else 'Above-lip segment exceeds six seconds. Possible spectator.'))
```

Inside `find_jumps`: Run this operation: `rejected.append`: add an item to the end of this list. Arguments: `dict`: create a dictionary from the named fields. Arguments: start = `start`; end = `end`; reason = `'No below-lip takeoff evidence. Possible drop-in or missed tracking.'` when NOT `takeoff`; otherwise `'Above-lip segment exceeds six seconds. Possible spectator.'`.

### Line 65

```python
            continue
```

Inside `find_jumps`: Skip the rest of this loop iteration and try the next item. This rejects the current unsuitable detection, fit, or sample.

### Line 66

```python
        values = np.array([samples[index]['height_px'] for index in group])
```

Inside `find_jumps`: Store the result in `values`: `np.array`: put the supplied values into a numerical array. Arguments: produce `samples[index]['height_px']`, for each index in `group`. This is assignment, not an equality check.

### Line 67

```python
        smoothed = np.array([np.median(values[max(0, i - 1):i + 2]) for i in range(len(values))])
```

Inside `find_jumps`: Store the result in `smoothed`: `np.array`: put the supplied values into a numerical array. Arguments: produce `np.median`: take the middle value after sorting, reducing the effect of one extreme value. Arguments: `values[max(0, i - 1):i + 2]`, for each i in `range`: produce integer loop positions, excluding the upper bound. Arguments: `len`: count items. Arguments: `values`. This is assignment, not an equality check.

### Line 68

```python
        near_peak = np.flatnonzero(smoothed >= smoothed.max() * 0.95)
```

Inside `find_jumps`: Store the result in `near_peak`: `np.flatnonzero`: return positions at which an array is nonzero or true. Arguments: `smoothed` is at least (`smoothed.max`: find the largest array value along the specified axis. No arguments are supplied times `0.95`). This is assignment, not an equality check.

### Line 69

```python
        chosen = int(min(near_peak, key=lambda i: abs(values[i] - smoothed[i])))
```

Inside `find_jumps`: Store the result in `chosen`: `int`: convert a value to a whole number. Arguments: `min`: choose the smallest value, or the item with the smallest key. Arguments: `near_peak`; key = a short function taking `i` and returning `abs`: call this function with the supplied arguments. Arguments: (`values[i]` minus `smoothed[i]`). This is assignment, not an equality check.

### Line 70

```python
        peak = samples[group[chosen]]
```

Inside `find_jumps`: Store the result in `peak`: `samples[group[chosen]]`. This is assignment, not an equality check.

### Line 71

```python
        if peak['confidence'] < 0.20 or peak['person'].get('motion', 1) < 0.10:
```

Inside `find_jumps`: Run the indented block only when this condition is true: `peak['confidence']` is less than `0.2` OR `peak['person'].get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'motion'`; `1` is less than `0.1`. Other branches handle the remaining case.

### Line 72

```python
            if rejected is not None:
```

Inside `find_jumps`: Run the indented block only when this condition is true: `rejected` is not the same object as `None`. Other branches handle the remaining case.

### Line 73

```python
                rejected.append(dict(start=start, end=end, reason='Peak has weak hip/lip evidence or little motion relative to the background.'))
```

Inside `find_jumps`: Run this operation: `rejected.append`: add an item to the end of this list. Arguments: `dict`: create a dictionary from the named fields. Arguments: start = `start`; end = `end`; reason = `'Peak has weak hip/lip evidence or little motion relative to the background.'`.

### Line 74

```python
            continue
```

Inside `find_jumps`: Skip the rest of this loop iteration and try the next item. This rejects the current unsuitable detection, fit, or sample.

### Line 75

```python
        reasons = ['Camera scale and vertical direction are not calibrated.']
```

Inside `find_jumps`: Store the result in `reasons`: list containing `'Camera scale and vertical direction are not calibrated.'`. This is assignment, not an equality check.

### Line 76

```python
        if single:
```

Inside `find_jumps`: Run the indented block only when this condition is true: `single`. Other branches handle the remaining case.

### Line 77

```python
            reasons.append('Only one sampled frame supports this candidate. Rescan this interval at six samples per second.')
```

Inside `find_jumps`: Run this operation: `reasons.append`: add an item to the end of this list. Arguments: `'Only one sampled frame supports this candidate. Rescan this interval at six samples per second.'`.

### Line 78

```python
        if end - start > 8:
```

Inside `find_jumps`: Run the indented block only when this condition is true: (`end` minus `start`) is greater than `8`. Other branches handle the remaining case.

### Line 79

```python
            reasons.append('Long above-lip segment; possible spectator or wrong line.')
```

Inside `find_jumps`: Run this operation: `reasons.append`: add an item to the end of this list. Arguments: `'Long above-lip segment; possible spectator or wrong line.'`.

### Line 80

```python
        if any(samples[index]['person'].get('ambiguous') for index in group):
```

Inside `find_jumps`: Run the indented block only when this condition is true: `any`: check whether at least one supplied condition is true. Arguments: produce `samples[index]['person'].get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'ambiguous'`, for each index in `group`. Other branches handle the remaining case.

### Line 81

```python
            reasons.append('More than one person could be the athlete.')
```

Inside `find_jumps`: Run this operation: `reasons.append`: add an item to the end of this list. Arguments: `'More than one person could be the athlete.'`.

### Line 82

```python
        if peak['lip']['extrapolated']:
```

Inside `find_jumps`: Run the indented block only when this condition is true: `peak['lip']['extrapolated']`. Other branches handle the remaining case.

### Line 83

```python
            reasons.append('Lip was extended beyond its visible support.')
```

Inside `find_jumps`: Run this operation: `reasons.append`: add an item to the end of this list. Arguments: `'Lip was extended beyond its visible support.'`.

### Line 84

```python
        if peak['confidence'] < 0.55:
```

Inside `find_jumps`: Run the indented block only when this condition is true: `peak['confidence']` is less than `0.55`. Other branches handle the remaining case.

### Line 85

```python
            reasons.append('Weak hip or lip evidence at the peak.')
```

Inside `find_jumps`: Run this operation: `reasons.append`: add an item to the end of this list. Arguments: `'Weak hip or lip evidence at the peak.'`.

### Line 86

```python
        if group[0] == 0 or group[-1] == len(samples) - 1:
```

Inside `find_jumps`: Run the indented block only when this condition is true: `group[0]` equals `0` OR `group[-1]` equals (`len`: count items. Arguments: `samples` minus `1`). Other branches handle the remaining case.

### Line 87

```python
            reasons.append('Candidate touches an analysis boundary.')
```

Inside `find_jumps`: Run this operation: `reasons.append`: add an item to the end of this list. Arguments: `'Candidate touches an analysis boundary.'`.

### Line 88

```python
        jumps.append(dict(id=len(jumps) + 1, start=round(start, 3), end=round(end, 3), peak_time=peak['time'], frame=peak['frame'], height_px=round(peak['height_px'], 2), height_m=None, confidence=round(peak['confidence'], 3), reviewed=False, excluded=False, reasons=reasons, sample_index=group[chosen], scale=None))
```

Inside `find_jumps`: Run this operation: `jumps.append`: add an item to the end of this list. Arguments: `dict`: create a dictionary from the named fields. Arguments: id = (`len`: count items. Arguments: `jumps` plus `1`); start = `round`: round a number to the requested precision. Arguments: `start`; `3`; end = `round`: round a number to the requested precision. Arguments: `end`; `3`; peak_time = `peak['time']`; frame = `peak['frame']`; height_px = `round`: round a number to the requested precision. Arguments: `peak['height_px']`; `2`; height_m = `None`; confidence = `round`: round a number to the requested precision. Arguments: `peak['confidence']`; `3`; reviewed = `False`; excluded = `False`; reasons = `reasons`; sample_index = `group[chosen]`; scale = `None`.

### Line 89

```python
    run, number, previous_end = 0, 0, None
```

Inside `find_jumps`: Store the result in `(run, number, previous_end)`: tuple containing `0`; `0`; `None`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 90

```python
    for jump in jumps:
```

Inside `find_jumps`: Repeat the following indented block for each `jump` from `jumps`. Tuple targets unpack each loop item.

### Line 91

```python
        if previous_end is None or jump['start'] - previous_end > 15:
```

Inside `find_jumps`: Run the indented block only when this condition is true: `previous_end` is the same object as `None` OR (`jump['start']` minus `previous_end`) is greater than `15`. Other branches handle the remaining case.

### Line 92

```python
            run += 1
```

Inside `find_jumps`: Update `run` using its old value plus `1`.

### Line 93

```python
            number = 0
```

Inside `find_jumps`: Store the result in `number`: `0`. This is assignment, not an equality check.

### Line 94

```python
        number += 1
```

Inside `find_jumps`: Update `number` using its old value plus `1`.

### Line 95

```python
        jump.update(run=run, jump_in_run=number)
```

Inside `find_jumps`: Run this operation: `jump.update`: replace or add the supplied named fields. Arguments: run = `run`; jump_in_run = `number`.

### Line 96

```python
        previous_end = jump['end']
```

Inside `find_jumps`: Store the result in `previous_end`: `jump['end']`. This is assignment, not an equality check.

### Line 97

```python
    return jumps
```

Inside `find_jumps`: End this function now and send back `jumps`. A bare return sends None.

### Line 98

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 99

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 100

```python
def save_report(report, folder):
```

Define `save_report(report, folder)`. Its job: Atomically save the session so partial runs can still be inspected. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 101

```python
    """Atomically save the session so partial runs can still be inspected."""
```

Inside `save_report`: Documentation string: Atomically save the session so partial runs can still be inspected. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 102

```python
    folder = Path(folder)
```

Inside `save_report`: Store the result in `folder`: `Path`: create a filesystem path object. Arguments: `folder`. This is assignment, not an equality check.

### Line 103

```python
    folder.mkdir(parents=True, exist_ok=True)
```

Inside `save_report`: Run this operation: `folder.mkdir`: create the folder, optionally creating parents and accepting an existing folder. Arguments: parents = `True`; exist_ok = `True`.

### Line 104

```python
    temporary = folder / 'report.tmp'
```

Inside `save_report`: Store the result in `temporary`: (`folder` divided by `'report.tmp'`). This is assignment, not an equality check.

### Line 105

```python
    temporary.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
```

Inside `save_report`: Run this operation: `temporary.write_text`: write text to a file with the selected encoding. Arguments: `json.dumps`: serialize dictionaries and lists to JSON text. Arguments: `report`; indent = `2`; allow_nan = `False`; encoding = `'utf-8'`.

### Line 106

```python
    temporary.replace(folder / 'report.json')
```

Inside `save_report`: Run this operation: `temporary.replace`: replace the target path atomically on this filesystem, or replace matching text in a string. Arguments: (`folder` divided by `'report.json'`).

### Line 107

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 108

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 109

```python
def export_csv(report, path):
```

Define `export_csv(report, path)`. Its job: Export accepted and excluded candidates with their review status. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 110

```python
    """Export accepted and excluded candidates with their review status."""
```

Inside `export_csv`: Documentation string: Export accepted and excluded candidates with their review status. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 111

```python
    columns = ['jump', 'run', 'jump_in_run', 'start_seconds', 'end_seconds', 'peak_seconds', 'frame', 'height_px', 'estimated_height_m', 'pixels_per_metre', 'confidence', 'reviewed', 'excluded', 'notes', 'calibration']
```

Inside `export_csv`: Store the result in `columns`: list containing `'jump'`; `'run'`; `'jump_in_run'`; `'start_seconds'`; `'end_seconds'`; `'peak_seconds'`; `'frame'`; `'height_px'`; `'estimated_height_m'`; `'pixels_per_metre'`; `'confidence'`; `'reviewed'`; `'excluded'`; `'notes'`; `'calibration'`. This is assignment, not an equality check.

### Line 112

```python
    with open(path, 'w', newline='', encoding='utf-8-sig') as output:
```

Inside `export_csv`: Enter managed resources: `open`: open a file with the supplied mode and encoding. Arguments: `path`; `'w'`; newline = `''`; encoding = `'utf-8-sig'` stored as `output`. The resources are closed or restored when this block ends, including after errors.

### Line 113

```python
        writer = csv.writer(output)
```

Inside `export_csv`: Store the result in `writer`: `csv.writer`: create a CSV row writer. Arguments: `output`. This is assignment, not an equality check.

### Line 114

```python
        writer.writerow(columns)
```

Inside `export_csv`: Run this operation: `writer.writerow`: write one CSV row with proper quoting. Arguments: `columns`.

### Line 115

```python
        for jump in report['jumps']:
```

Inside `export_csv`: Repeat the following indented block for each `jump` from `report['jumps']`. Tuple targets unpack each loop item.

### Line 116

```python
            writer.writerow([jump['id'], jump.get('run', ''), jump.get('jump_in_run', ''), jump['start'], jump['end'], jump['peak_time'], jump['frame'], jump['height_px'], '' if jump['height_m'] is None else jump['height_m'], '' if jump['scale'] is None else jump['scale'], jump['confidence'], jump['reviewed'], jump['excluded'], ' '.join(jump['reasons']), json.dumps(jump.get('calibration'))])
```

Inside `export_csv`: Run this operation: `writer.writerow`: write one CSV row with proper quoting. Arguments: list containing `jump['id']`; `jump.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'run'`; `''`; `jump.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'jump_in_run'`; `''`; `jump['start']`; `jump['end']`; `jump['peak_time']`; `jump['frame']`; `jump['height_px']`; `''` when `jump['height_m']` is the same object as `None`; otherwise `jump['height_m']`; `''` when `jump['scale']` is the same object as `None`; otherwise `jump['scale']`; `jump['confidence']`; `jump['reviewed']`; `jump['excluded']`; `' '.join`: call this function with the supplied arguments. Arguments: `jump['reasons']`; `json.dumps`: serialize dictionaries and lists to JSON text. Arguments: `jump.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'calibration'`.

### Line 117

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 118

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 119

```python
def export_skipped(report, path):
```

Define `export_skipped(report, path)`. Its job: Make rejected interval times readable without opening the JSON report. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 120

```python
    """Make rejected interval times readable without opening the JSON report."""
```

Inside `export_skipped`: Documentation string: Make rejected interval times readable without opening the JSON report. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 121

```python
    with open(path, 'w', newline='', encoding='utf-8-sig') as output:
```

Inside `export_skipped`: Enter managed resources: `open`: open a file with the supplied mode and encoding. Arguments: `path`; `'w'`; newline = `''`; encoding = `'utf-8-sig'` stored as `output`. The resources are closed or restored when this block ends, including after errors.

### Line 122

```python
        writer = csv.writer(output)
```

Inside `export_skipped`: Store the result in `writer`: `csv.writer`: create a CSV row writer. Arguments: `output`. This is assignment, not an equality check.

### Line 123

```python
        writer.writerow(['start_seconds', 'end_seconds', 'reason'])
```

Inside `export_skipped`: Run this operation: `writer.writerow`: write one CSV row with proper quoting. Arguments: list containing `'start_seconds'`; `'end_seconds'`; `'reason'`.

### Line 124

```python
        for segment in report.get('rejected_segments', []):
```

Inside `export_skipped`: Repeat the following indented block for each `segment` from `report.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'rejected_segments'`; an empty list `[]`. Tuple targets unpack each loop item.

### Line 125

```python
            writer.writerow([segment['start'], segment['end'], segment['reason']])
```

Inside `export_skipped`: Run this operation: `writer.writerow`: write one CSV row with proper quoting. Arguments: list containing `segment['start']`; `segment['end']`; `segment['reason']`.

### Line 126

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 127

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 128

```python
def analyse(source, start=0, end=0, sample_rate=6, progress=lambda data: None, preview=lambda frame: None, cancelled=lambda: False, folder=None, model_path=None):
```

Define `analyse(source, start=0, end=0, sample_rate=6, progress=lambda data: None, preview=lambda frame: None, cancelled=lambda: False, folder=None, model_path=None)`. Its job: Sample the requested range without holding the whole movie in memory. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 129

```python
    """Sample the requested range without holding the whole movie in memory."""
```

Inside `analyse`: Documentation string: Sample the requested range without holding the whole movie in memory. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 130

```python
    source = str(source)
```

Inside `analyse`: Store the result in `source`: `str`: convert a value to text. Arguments: `source`. This is assignment, not an equality check.

### Line 131

```python
    if not source.startswith(('https://', 'http://')):
```

Inside `analyse`: Run the indented block only when this condition is true: NOT `source.startswith`: call this function with the supplied arguments. Arguments: tuple containing `'https://'`; `'http://'`. Other branches handle the remaining case.

### Line 132

```python
        source = str(Path(source).expanduser().resolve())
```

Inside `analyse`: Store the result in `source`: `str`: convert a value to text. Arguments: `Path(source).expanduser().resolve`: convert the path to an absolute resolved path. No arguments are supplied. This is assignment, not an equality check.

### Line 133

```python
    if not 1 <= sample_rate <= 30 or not math.isfinite(start) or not math.isfinite(end) or start < 0 or end < 0:
```

Inside `analyse`: Run the indented block only when this condition is true: NOT `1` is at most `sample_rate` and is at most `30` OR NOT `math.isfinite`: check that a number is neither infinite nor NaN. Arguments: `start` OR NOT `math.isfinite`: check that a number is neither infinite nor NaN. Arguments: `end` OR `start` is less than `0` OR `end` is less than `0`. Other branches handle the remaining case.

### Line 134

```python
        raise ValueError('Use 1 to 30 samples per second and nonnegative start/end times.')
```

Inside `analyse`: Stop this operation by raising an exception: `ValueError`: call this function with the supplied arguments. Arguments: `'Use 1 to 30 samples per second and nonnegative start/end times.'`. A matching except block can handle it.

### Line 135

```python
    model_path = model_path or ensure_model(lambda text: progress(dict(message=text, percent=0)), cancelled)
```

Inside `analyse`: Store the result in `model_path`: `model_path` OR `ensure_model`: find or download model weights and verify their SHA-256 hash. Arguments: a short function taking `text` and returning `progress`: call this function with the supplied arguments. Arguments: `dict`: create a dictionary from the named fields. Arguments: message = `text`; percent = `0`; `cancelled`. This is assignment, not an equality check.

### Line 136

```python
    detector = PoseDetector(model_path)
```

Inside `analyse`: Store the result in `detector`: `PoseDetector`: call this function with the supplied arguments. Arguments: `model_path`. This is assignment, not an equality check.

### Line 137

```python
    capture, fps, count = open_video(source)
```

Inside `analyse`: Store the result in `(capture, fps, count)`: `open_video`: open a source through FFmpeg and validate its video metadata. Arguments: `source`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 138

```python
    duration = count / fps
```

Inside `analyse`: Store the result in `duration`: (`count` divided by `fps`). This is assignment, not an equality check.

### Line 139

```python
    end = min(end, duration) if end else duration
```

Inside `analyse`: Store the result in `end`: `min`: choose the smallest value, or the item with the smallest key. Arguments: `end`; `duration` when `end`; otherwise `duration`. This is assignment, not an equality check.

### Line 140

```python
    if start >= end:
```

Inside `analyse`: Run the indented block only when this condition is true: `start` is at least `end`. Other branches handle the remaining case.

### Line 141

```python
        capture.release()
```

Inside `analyse`: Run this operation: `capture.release`: close the video reader or finalize the video writer. No arguments are supplied.

### Line 142

```python
        raise ValueError('The start time must be before the end of the selected range.')
```

Inside `analyse`: Stop this operation by raising an exception: `ValueError`: call this function with the supplied arguments. Arguments: `'The start time must be before the end of the selected range.'`. A matching except block can handle it.

### Line 143

```python
    folder = Path(folder) if folder else data_folder() / 'sessions' / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
```

Inside `analyse`: Store the result in `folder`: `Path`: create a filesystem path object. Arguments: `folder` when `folder`; otherwise ((`data_folder`: get a writable folder for this user's models and sessions. No arguments are supplied divided by `'sessions'`) divided by `datetime.now().strftime`: format the current date and time into a unique session-folder name. Arguments: `'%Y%m%d-%H%M%S-%f'`). This is assignment, not an equality check.

### Line 144

```python
    folder.mkdir(parents=True, exist_ok=True)
```

Inside `analyse`: Run this operation: `folder.mkdir`: create the folder, optionally creating parents and accepting an existing folder. Arguments: parents = `True`; exist_ok = `True`.

### Line 145

```python
    report = dict(version=2, source=source, fps=fps, frame_count=count, width=0, height=0, start=start, end=end, sample_rate=sample_rate, state='running', complete=False, next_frame=round(start * fps), samples=[], jumps=[], errors=[], folder=str(folder), model_sha256='04f6d2416266f2aba6c5ba8b26de33ed9eba3279f972ac02e33f9f1366547586')
```

Inside `analyse`: Store the result in `report`: `dict`: create a dictionary from the named fields. Arguments: version = `2`; source = `source`; fps = `fps`; frame_count = `count`; width = `0`; height = `0`; start = `start`; end = `end`; sample_rate = `sample_rate`; state = `'running'`; complete = `False`; next_frame = `round`: round a number to the requested precision. Arguments: (`start` times `fps`); samples = an empty list `[]`; jumps = an empty list `[]`; errors = an empty list `[]`; folder = `str`: convert a value to text. Arguments: `folder`; model_sha256 = `'04f6d2416266f2aba6c5ba8b26de33ed9eba3279f972ac02e33f9f1366547586'`. This is assignment, not an equality check.

### Line 146

```python
    first = round(start * fps)
```

Inside `analyse`: Store the result in `first`: `round`: round a number to the requested precision. Arguments: (`start` times `fps`). This is assignment, not an equality check.

### Line 147

```python
    last = min(count, math.ceil(end * fps))
```

Inside `analyse`: Store the result in `last`: `min`: choose the smallest value, or the item with the smallest key. Arguments: `count`; `math.ceil`: call this function with the supplied arguments. Arguments: (`end` times `fps`). This is assignment, not an equality check.

### Line 148

```python
    stride = max(1, round(fps / sample_rate))
```

Inside `analyse`: Store the result in `stride`: `max`: choose the largest value, or the item with the largest key. Arguments: `1`; `round`: round a number to the requested precision. Arguments: (`fps` divided by `sample_rate`). This is assignment, not an equality check.

### Line 149

```python
    report['effective_sample_rate'] = fps / stride
```

Inside `analyse`: Store the result in `report['effective_sample_rate']`: (`fps` divided by `stride`). This is assignment, not an equality check.

### Line 150

```python
    report['detector_revision'] = 'motion-roi-takeoff-v2'
```

Inside `analyse`: Store the result in `report['detector_revision']`: `'motion-roi-takeoff-v2'`. This is assignment, not an equality check.

### Line 151

```python
    report['grouping_revision'] = 'takeoff-v3'
```

Inside `analyse`: Store the result in `report['grouping_revision']`: `'takeoff-v3'`. This is assignment, not an equality check.

### Line 152

```python
    report['pipe_dimensions'] = PIPE_DIMENSIONS.copy()
```

Inside `analyse`: Store the result in `report['pipe_dimensions']`: `PIPE_DIMENSIONS.copy`: make a separate copy so later drawing or changes do not overwrite the original. No arguments are supplied. This is assignment, not an equality check.

### Line 153

```python
    report['run_note'] = 'Runs are separated by gaps over 15 seconds between jump candidates. These are riding sequences, not identified athlete names. Replays can appear again.'
```

Inside `analyse`: Store the result in `report['run_note']`: `'Runs are separated by gaps over 15 seconds between jump candidates. These are riding sequences, not identified athlete names. Replays can appear again.'`. This is assignment, not an equality check.

### Line 154

```python
    capture.set(cv2.CAP_PROP_POS_FRAMES, first)
```

Inside `analyse`: Run this operation: `capture.set`: set a video reader property, such as its next frame position. Arguments: `cv2.CAP_PROP_POS_FRAMES`; `first`.

### Line 155

```python
    previous, previous_image, previous_frame = None, None, None
```

Inside `analyse`: Store the result in `(previous, previous_image, previous_frame)`: tuple containing `None`; `None`; `None`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 156

```python
    started = time.monotonic()
```

Inside `analyse`: Store the result in `started`: `time.monotonic`: read a clock suitable for elapsed time that does not jump with wall-clock changes. No arguments are supplied. This is assignment, not an equality check.

### Line 157

```python
    index, failures, measured = first, 0, 0
```

Inside `analyse`: Store the result in `(index, failures, measured)`: tuple containing `first`; `0`; `0`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 158

```python
    writer = None
```

Inside `analyse`: Store the result in `writer`: `None`. This is assignment, not an equality check.

### Line 159

```python
    try:
```

Inside `analyse`: Begin an operation with explicit error handling. The following except clauses handle failures; finally performs cleanup even after a return or error.

### Line 160

```python
        while index < last and not cancelled():
```

Inside `analyse`: Keep repeating the indented block while `index` is less than `last` AND NOT `cancelled`: call this function with the supplied arguments. No arguments are supplied. The body must advance or stop the loop.

### Line 161

```python
            ok, frame = capture.read()
```

Inside `analyse`: Store the result in `(ok, frame)`: `capture.read`: read the next frame or next byte chunk from this resource. No arguments are supplied. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 162

```python
            if not ok:
```

Inside `analyse`: Run the indented block only when this condition is true: NOT `ok`. Other branches handle the remaining case.

### Line 163

```python
                failures += 1
```

Inside `analyse`: Update `failures` using its old value plus `1`.

### Line 164

```python
                report['errors'].append(f'Could not decode frame {index}.')
```

Inside `analyse`: Run this operation: `report['errors'].append`: add an item to the end of this list. Arguments: formatted text `f'Could not decode frame {index}.'`. Inserted values: index.

### Line 165

```python
                if failures >= 3:
```

Inside `analyse`: Run the indented block only when this condition is true: `failures` is at least `3`. Other branches handle the remaining case.

### Line 166

```python
                    report['state'] = 'read_error'
```

Inside `analyse`: Store the result in `report['state']`: `'read_error'`. This is assignment, not an equality check.

### Line 167

```python
                    break
```

Inside `analyse`: End the nearest enclosing loop immediately. Processing continues after the loop.

### Line 168

```python
                index += stride
```

Inside `analyse`: Update `index` using its old value plus `stride`.

### Line 169

```python
                capture.set(cv2.CAP_PROP_POS_FRAMES, index)
```

Inside `analyse`: Run this operation: `capture.set`: set a video reader property, such as its next frame position. Arguments: `cv2.CAP_PROP_POS_FRAMES`; `index`.

### Line 170

```python
                continue
```

Inside `analyse`: Skip the rest of this loop iteration and try the next item. This rejects the current unsuitable detection, fit, or sample.

### Line 171

```python
            failures = 0
```

Inside `analyse`: Store the result in `failures`: `0`. This is assignment, not an equality check.

### Line 172

```python
            report['height'], report['width'] = frame.shape[:2]
```

Inside `analyse`: Store the result in `(report['height'], report['width'])`: `frame.shape[:2]`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 173

```python
            if writer is None:
```

Inside `analyse`: Run the indented block only when this condition is true: `writer` is the same object as `None`. Other branches handle the remaining case.

### Line 174

```python
                ratio = min(1, 960 / frame.shape[1])
```

Inside `analyse`: Store the result in `ratio`: `min`: choose the smallest value, or the item with the smallest key. Arguments: `1`; (`960` divided by `frame.shape[1]`). This is assignment, not an equality check.

### Line 175

```python
                review_size = (int(frame.shape[1] * ratio) // 2 * 2, int(frame.shape[0] * ratio) // 2 * 2)
```

Inside `analyse`: Store the result in `review_size`: tuple containing ((`int`: convert a value to a whole number. Arguments: (`frame.shape[1]` times `ratio`) floor-divided by `2`) times `2`); ((`int`: convert a value to a whole number. Arguments: (`frame.shape[0]` times `ratio`) floor-divided by `2`) times `2`). This is assignment, not an equality check.

### Line 176

```python
                writer = cv2.VideoWriter(str(folder / 'review.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), fps / stride, review_size)
```

Inside `analyse`: Store the result in `writer`: `cv2.VideoWriter`: create a video file encoder. Arguments: `str`: convert a value to text. Arguments: (`folder` divided by `'review.mp4'`); `cv2.VideoWriter_fourcc`: turn the four codec letters into OpenCV's codec identifier. Arguments: `*'mp4v'`; (`fps` divided by `stride`); `review_size`. This is assignment, not an equality check.

### Line 177

```python
                report['review_video'] = 'review.mp4' if writer.isOpened() else None
```

Inside `analyse`: Store the result in `report['review_video']`: `'review.mp4'` when `writer.isOpened`: check whether the video resource opened successfully. No arguments are supplied; otherwise `None`. This is assignment, not an equality check.

### Line 178

```python
                report['review_note'] = 'Sampled, silent review video. Frame timestamps refer to the source. Later point corrections appear in snapshots and CSV only.'
```

Inside `analyse`: Store the result in `report['review_note']`: `'Sampled, silent review video. Frame timestamps refer to the source. Later point corrections appear in snapshots and CSV only.'`. This is assignment, not an equality check.

### Line 179

```python
            tiny = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (64, 36)).astype(float)
```

Inside `analyse`: Store the result in `tiny`: `cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (64, 36)).astype`: convert array values to the requested numeric type. Arguments: `float`. This is assignment, not an equality check.

### Line 180

```python
            cut = previous_image is not None and np.abs(tiny - previous_image).mean() > 45
```

Inside `analyse`: Store the result in `cut`: `previous_image` is not the same object as `None` AND `np.abs(tiny - previous_image).mean`: calculate the arithmetic mean of array values. No arguments are supplied is greater than `45`. This is assignment, not an equality check.

### Line 181

```python
            if cut:
```

Inside `analyse`: Run the indented block only when this condition is true: `cut`. Other branches handle the remaining case.

### Line 182

```python
                previous = None
```

Inside `analyse`: Store the result in `previous`: `None`. This is assignment, not an equality check.

### Line 183

```python
            field = motion_field(previous_frame, frame) if not cut else None
```

Inside `analyse`: Store the result in `field`: `motion_field`: track image corners and remove common camera pan, rotation, and zoom. Arguments: `previous_frame`; `frame` when NOT `cut`; otherwise `None`. This is assignment, not an equality check.

### Line 184

```python
            people = detector.detect(frame, motion=field)
```

Inside `analyse`: Store the result in `people`: `detector.detect`: combine the full image with magnified moving crop detections at four rotations. Arguments: `frame`; motion = `field`. This is assignment, not an equality check.

### Line 185

```python
            if field is not None:
```

Inside `analyse`: Run the indented block only when this condition is true: `field` is not the same object as `None`. Other branches handle the remaining case.

### Line 186

```python
                score_motion(previous_frame, frame, people, field)
```

Inside `analyse`: Run this operation: `score_motion`: score residual movement inside each person using the camera compensated feature field. Arguments: `previous_frame`; `frame`; `people`; `field`.

### Line 187

```python
            person = choose_athlete(people, frame.shape, previous)
```

Inside `analyse`: Store the result in `person`: `choose_athlete`: rank person hypotheses by prominence, central position, and continuity. Arguments: `people`; `frame.shape`; `previous`. This is assignment, not an equality check.

### Line 188

```python
            lip = find_lip(frame, person['hip'], person['box']) if person else None
```

Inside `analyse`: Store the result in `lip`: `find_lip`: find supporting blue pixels near the hip and fit a short robust reference line. Arguments: `frame`; `person['hip']`; `person['box']` when `person`; otherwise `None`. This is assignment, not an equality check.

### Line 189

```python
            height_px = lip['y'] - person['hip'][1] if lip else None
```

Inside `analyse`: Store the result in `height_px`: (`lip['y']` minus `person['hip'][1]`) when `lip`; otherwise `None`. This is assignment, not an equality check.

### Line 190

```python
            confidence = min(person['score'], person['hip_score'], lip['score']) if lip else 0
```

Inside `analyse`: Store the result in `confidence`: `min`: choose the smallest value, or the item with the smallest key. Arguments: `person['score']`; `person['hip_score']`; `lip['score']` when `lip`; otherwise `0`. This is assignment, not an equality check.

### Line 191

```python
            if lip and abs(height_px) > frame.shape[0] * 0.8:
```

Inside `analyse`: Run the indented block only when this condition is true: `lip` AND `abs`: call this function with the supplied arguments. Arguments: `height_px` is greater than (`frame.shape[0]` times `0.8`). Other branches handle the remaining case.

### Line 192

```python
                height_px = None
```

Inside `analyse`: Store the result in `height_px`: `None`. This is assignment, not an equality check.

### Line 193

```python
                confidence = 0
```

Inside `analyse`: Store the result in `confidence`: `0`. This is assignment, not an equality check.

### Line 194

```python
            status = 'Measured image gap' if height_px is not None else ('Lip not clear' if person else 'Athlete not found')
```

Inside `analyse`: Store the result in `status`: `'Measured image gap'` when `height_px` is not the same object as `None`; otherwise `'Lip not clear'` when `person`; otherwise `'Athlete not found'`. This is assignment, not an equality check.

### Line 195

```python
            sample = dict(frame=index, time=round(index / fps, 3), person=person, lip=lip, height_px=height_px, confidence=float(confidence), status=status, cut=bool(cut))
```

Inside `analyse`: Store the result in `sample`: `dict`: create a dictionary from the named fields. Arguments: frame = `index`; time = `round`: round a number to the requested precision. Arguments: (`index` divided by `fps`); `3`; person = `person`; lip = `lip`; height_px = `height_px`; confidence = `float`: convert a value to a decimal number. Arguments: `confidence`; status = `status`; cut = `bool`: convert a condition to a plain Python True or False. Arguments: `cut`. This is assignment, not an equality check.

### Line 196

```python
            report['samples'].append(sample)
```

Inside `analyse`: Run this operation: `report['samples'].append`: add an item to the end of this list. Arguments: `sample`.

### Line 197

```python
            measured += height_px is not None
```

Inside `analyse`: Update `measured` using its old value plus `height_px` is not the same object as `None`.

### Line 198

```python
            marked = annotate(frame, sample)
```

Inside `analyse`: Store the result in `marked`: `annotate`: copy an image and draw the box, body points, hip, lip, and measurement. Arguments: `frame`; `sample`. This is assignment, not an equality check.

### Line 199

```python
            cv2.putText(marked, f'Source {index / fps:.2f}s', (24, frame.shape[0] - 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
```

Inside `analyse`: Run this operation: `cv2.putText`: draw the supplied text on the image. Arguments: `marked`; formatted text `f'Source {index / fps:.2f}s'`. Inserted values: index / fps, format f'.2f'; tuple containing `24`; (`frame.shape[0]` minus `22`); `cv2.FONT_HERSHEY_SIMPLEX`; `0.6`; tuple containing `255`; `255`; `255`; `2`.

### Line 200

```python
            if writer.isOpened():
```

Inside `analyse`: Run the indented block only when this condition is true: `writer.isOpened`: check whether the video resource opened successfully. No arguments are supplied. Other branches handle the remaining case.

### Line 201

```python
                writer.write(cv2.resize(marked, review_size))
```

Inside `analyse`: Run this operation: `writer.write`: write bytes or an encoded frame to the open output. Arguments: `cv2.resize`: resize an image to the requested width and height. Arguments: `marked`; `review_size`.

### Line 202

```python
            previous, previous_image = person, tiny
```

Inside `analyse`: Store the result in `(previous, previous_image)`: tuple containing `person`; `tiny`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 203

```python
            previous_frame = frame
```

Inside `analyse`: Store the result in `previous_frame`: `frame`. This is assignment, not an equality check.

### Line 204

```python
            report['next_frame'] = min(last, index + stride)
```

Inside `analyse`: Store the result in `report['next_frame']`: `min`: choose the smallest value, or the item with the smallest key. Arguments: `last`; (`index` plus `stride`). This is assignment, not an equality check.

### Line 205

```python
            percent = (index - first + 1) / max(1, last - first) * 100
```

Inside `analyse`: Store the result in `percent`: ((((`index` minus `first`) plus `1`) divided by `max`: choose the largest value, or the item with the largest key. Arguments: `1`; (`last` minus `first`)) times `100`). This is assignment, not an equality check.

### Line 206

```python
            elapsed = time.monotonic() - started
```

Inside `analyse`: Store the result in `elapsed`: (`time.monotonic`: read a clock suitable for elapsed time that does not jump with wall-clock changes. No arguments are supplied minus `started`). This is assignment, not an equality check.

### Line 207

```python
            remaining = elapsed * (100 - percent) / max(0.01, percent)
```

Inside `analyse`: Store the result in `remaining`: ((`elapsed` times (`100` minus `percent`)) divided by `max`: choose the largest value, or the item with the largest key. Arguments: `0.01`; `percent`). This is assignment, not an equality check.

### Line 208

```python
            if len(report['samples']) % 3 == 1:
```

Inside `analyse`: Run the indented block only when this condition is true: (`len`: count items. Arguments: `report['samples']` modulo `3`) equals `1`. Other branches handle the remaining case.

### Line 209

```python
                preview(marked)
```

Inside `analyse`: Run this operation: `preview`: call this function with the supplied arguments. Arguments: `marked`.

### Line 210

```python
                progress(dict(percent=percent, time=sample['time'], samples=len(report['samples']), measured=measured, remaining=remaining, message=f"Analysing {sample['time']:.1f} seconds"))
```

Inside `analyse`: Run this operation: `progress`: call this function with the supplied arguments. Arguments: `dict`: create a dictionary from the named fields. Arguments: percent = `percent`; time = `sample['time']`; samples = `len`: count items. Arguments: `report['samples']`; measured = `measured`; remaining = `remaining`; message = formatted text `f"Analysing {sample['time']:.1f} seconds"`. Inserted values: sample['time'], format f'.1f'.

### Line 211

```python
            if len(report['samples']) % 500 == 0:
```

Inside `analyse`: Run the indented block only when this condition is true: (`len`: count items. Arguments: `report['samples']` modulo `500`) equals `0`. Other branches handle the remaining case.

### Line 212

```python
                report['jumps'] = find_jumps(report['samples'], sample_rate)
```

Inside `analyse`: Store the result in `report['jumps']`: `find_jumps`: group positive samples, require below-lip takeoff evidence, reject drop-ins, and number riding sequences. Arguments: `report['samples']`; `sample_rate`. This is assignment, not an equality check.

### Line 213

```python
                save_report(report, folder)
```

Inside `analyse`: Run this operation: `save_report`: write the complete JSON session through a temporary file. Arguments: `report`; `folder`.

### Line 214

```python
            for _ in range(min(stride - 1, last - index - 1)):
```

Inside `analyse`: Repeat the following indented block for each `_` from `range`: produce integer loop positions, excluding the upper bound. Arguments: `min`: choose the smallest value, or the item with the smallest key. Arguments: (`stride` minus `1`); ((`last` minus `index`) minus `1`). Tuple targets unpack each loop item.

### Line 215

```python
                if cancelled():
```

Inside `analyse`: Run the indented block only when this condition is true: `cancelled`: call this function with the supplied arguments. No arguments are supplied. Other branches handle the remaining case.

### Line 216

```python
                    break
```

Inside `analyse`: End the nearest enclosing loop immediately. Processing continues after the loop.

### Line 217

```python
                capture.grab()
```

Inside `analyse`: Run this operation: `capture.grab`: advance the video reader without converting the skipped image. No arguments are supplied.

### Line 218

```python
            index += stride
```

Inside `analyse`: Update `index` using its old value plus `stride`.

### Line 219

```python
        if cancelled():
```

Inside `analyse`: Run the indented block only when this condition is true: `cancelled`: call this function with the supplied arguments. No arguments are supplied. Other branches handle the remaining case.

### Line 220

```python
            report['state'] = 'stopped'
```

Inside `analyse`: Store the result in `report['state']`: `'stopped'`. This is assignment, not an equality check.

### Line 221

```python
        elif report['state'] == 'running':
```

Inside `analyse`: If earlier branches did not run, test this additional condition: `report['state'] == 'running'`.

### Line 222

```python
            report['state'] = 'complete'
```

Inside `analyse`: Store the result in `report['state']`: `'complete'`. This is assignment, not an equality check.

### Line 223

```python
            report['complete'] = True
```

Inside `analyse`: Store the result in `report['complete']`: `True`. This is assignment, not an equality check.

### Line 224

```python
        report['rejected_segments'] = []
```

Inside `analyse`: Store the result in `report['rejected_segments']`: an empty list `[]`. This is assignment, not an equality check.

### Line 225

```python
        report['jumps'] = find_jumps(report['samples'], sample_rate, report['rejected_segments'])
```

Inside `analyse`: Store the result in `report['jumps']`: `find_jumps`: group positive samples, require below-lip takeoff evidence, reject drop-ins, and number riding sequences. Arguments: `report['samples']`; `sample_rate`; `report['rejected_segments']`. This is assignment, not an equality check.

### Line 226

```python
        report['elapsed_seconds'] = round(time.monotonic() - started, 2)
```

Inside `analyse`: Store the result in `report['elapsed_seconds']`: `round`: round a number to the requested precision. Arguments: (`time.monotonic`: read a clock suitable for elapsed time that does not jump with wall-clock changes. No arguments are supplied minus `started`); `2`. This is assignment, not an equality check.

### Line 227

```python
        for jump in report['jumps']:
```

Inside `analyse`: Repeat the following indented block for each `jump` from `report['jumps']`. Tuple targets unpack each loop item.

### Line 228

```python
            if cancelled():
```

Inside `analyse`: Run the indented block only when this condition is true: `cancelled`: call this function with the supplied arguments. No arguments are supplied. Other branches handle the remaining case.

### Line 229

```python
                break
```

Inside `analyse`: End the nearest enclosing loop immediately. Processing continues after the loop.

### Line 230

```python
            capture.set(cv2.CAP_PROP_POS_FRAMES, jump['frame'])
```

Inside `analyse`: Run this operation: `capture.set`: set a video reader property, such as its next frame position. Arguments: `cv2.CAP_PROP_POS_FRAMES`; `jump['frame']`.

### Line 231

```python
            ok, frame = capture.read()
```

Inside `analyse`: Store the result in `(ok, frame)`: `capture.read`: read the next frame or next byte chunk from this resource. No arguments are supplied. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 232

```python
            if ok:
```

Inside `analyse`: Run the indented block only when this condition is true: `ok`. Other branches handle the remaining case.

### Line 233

```python
                filename = f"jump-{jump['id']:03}.jpg"
```

Inside `analyse`: Store the result in `filename`: formatted text `f"jump-{jump['id']:03}.jpg"`. Inserted values: jump['id'], format f'03'. This is assignment, not an equality check.

### Line 234

```python
                cv2.imwrite(str(folder / filename), annotate(frame, report['samples'][jump['sample_index']]))
```

Inside `analyse`: Run this operation: `cv2.imwrite`: encode and save an image at the supplied path. Arguments: `str`: convert a value to text. Arguments: (`folder` divided by `filename`); `annotate`: copy an image and draw the box, body points, hip, lip, and measurement. Arguments: `frame`; `report['samples'][jump['sample_index']]`.

### Line 235

```python
                jump['snapshot'] = filename
```

Inside `analyse`: Store the result in `jump['snapshot']`: `filename`. This is assignment, not an equality check.

### Line 236

```python
        save_report(report, folder)
```

Inside `analyse`: Run this operation: `save_report`: write the complete JSON session through a temporary file. Arguments: `report`; `folder`.

### Line 237

```python
        export_csv(report, folder / 'jumps.csv')
```

Inside `analyse`: Run this operation: `export_csv`: write candidate rows including their review and exclusion flags. Arguments: `report`; (`folder` divided by `'jumps.csv'`).

### Line 238

```python
        export_skipped(report, folder / 'skipped.csv')
```

Inside `analyse`: Run this operation: `export_skipped`: write rejected interval times and reasons into a separate review table. Arguments: `report`; (`folder` divided by `'skipped.csv'`).

### Line 239

```python
        return report
```

Inside `analyse`: End this function now and send back `report`. A bare return sends None.

### Line 240

```python
    except Exception as error:
```

Inside `analyse`: Handle the exception type(s) named here. `as error` stores the exception so a readable message can be shown or saved.

### Line 241

```python
        report['state'] = 'error'
```

Inside `analyse`: Store the result in `report['state']`: `'error'`. This is assignment, not an equality check.

### Line 242

```python
        report['errors'].append(str(error))
```

Inside `analyse`: Run this operation: `report['errors'].append`: add an item to the end of this list. Arguments: `str`: convert a value to text. Arguments: `error`.

### Line 243

```python
        report['jumps'] = find_jumps(report['samples'], sample_rate)
```

Inside `analyse`: Store the result in `report['jumps']`: `find_jumps`: group positive samples, require below-lip takeoff evidence, reject drop-ins, and number riding sequences. Arguments: `report['samples']`; `sample_rate`. This is assignment, not an equality check.

### Line 244

```python
        save_report(report, folder)
```

Inside `analyse`: Run this operation: `save_report`: write the complete JSON session through a temporary file. Arguments: `report`; `folder`.

### Line 245

```python
        raise
```

Inside `analyse`: Stop this operation by raising an exception: no explicit value. A matching except block can handle it.

### Line 246

```python
    finally:
```

Inside `analyse`: Always run the following cleanup block, whether processing succeeds, returns early, or raises an error.

### Line 247

```python
        capture.release()
```

Inside `analyse`: Run this operation: `capture.release`: close the video reader or finalize the video writer. No arguments are supplied.

### Line 248

```python
        if writer is not None:
```

Inside `analyse`: Run the indented block only when this condition is true: `writer` is not the same object as `None`. Other branches handle the remaining case.

### Line 249

```python
            writer.release()
```

Inside `analyse`: Run this operation: `writer.release`: close the video reader or finalize the video writer. No arguments are supplied.

## vision.py

Source SHA-256: `0878d61fd4e2dd0e19a01e039d54d286cec5cf411a3d43d1e125815ad9361f87`

### Line 1

```python
"""Find people, estimate hips, and fit a local blue lip in a video image."""
```

Documentation string: Find people, estimate hips, and fit a local blue lip in a video image. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 2

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 3

```python
import hashlib
```

Import modules: hashlib. Their functions become available through those module names.

### Line 4

```python
import os
```

Import modules: os. Their functions become available through those module names.

### Line 5

```python
from pathlib import Path
```

Import Path from `pathlib`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 6

```python
from urllib.request import urlopen
```

Import urlopen from `urllib.request`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 7

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 8

```python
import cv2
```

Import modules: cv2. Their functions become available through those module names.

### Line 9

```python
import numpy as np
```

Import modules: numpy under the short name np. Their functions become available through those module names.

### Line 10

```python
import onnxruntime as ort
```

Import modules: onnxruntime under the short name ort. Their functions become available through those module names.

### Line 11

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 12

```python
MODEL_URL = 'https://huggingface.co/Xenova/yolov8n-pose/resolve/main/onnx/model.onnx'
```

Store the result in `MODEL_URL`: `'https://huggingface.co/Xenova/yolov8n-pose/resolve/main/onnx/model.onnx'`. This is assignment, not an equality check.

### Line 13

```python
MODEL_SHA256 = '04f6d2416266f2aba6c5ba8b26de33ed9eba3279f972ac02e33f9f1366547586'
```

Store the result in `MODEL_SHA256`: `'04f6d2416266f2aba6c5ba8b26de33ed9eba3279f972ac02e33f9f1366547586'`. This is assignment, not an equality check.

### Line 14

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 15

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 16

```python
def data_folder():
```

Define `data_folder()`. Its job: Keep downloaded models and sessions in one user-writable folder. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 17

```python
    """Keep downloaded models and sessions in one user-writable folder."""
```

Inside `data_folder`: Documentation string: Keep downloaded models and sessions in one user-writable folder. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 18

```python
    folder = Path(os.getenv('LOCALAPPDATA', str(Path.home() / '.cache'))) / 'Lip'
```

Inside `data_folder`: Store the result in `folder`: (`Path`: create a filesystem path object. Arguments: `os.getenv`: call this function with the supplied arguments. Arguments: `'LOCALAPPDATA'`; `str`: convert a value to text. Arguments: (`Path.home`: call this function with the supplied arguments. No arguments are supplied divided by `'.cache'`) divided by `'Lip'`). This is assignment, not an equality check.

### Line 19

```python
    folder.mkdir(parents=True, exist_ok=True)
```

Inside `data_folder`: Run this operation: `folder.mkdir`: create the folder, optionally creating parents and accepting an existing folder. Arguments: parents = `True`; exist_ok = `True`.

### Line 20

```python
    return folder
```

Inside `data_folder`: End this function now and send back `folder`. A bare return sends None.

### Line 21

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 22

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 23

```python
def ensure_model(progress=lambda text: None, cancelled=lambda: False):
```

Define `ensure_model(progress=lambda text: None, cancelled=lambda: False)`. Its job: Use bundled weights or download the exact verified model once. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 24

```python
    """Use bundled weights or download the exact verified model once."""
```

Inside `ensure_model`: Documentation string: Use bundled weights or download the exact verified model once. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 25

```python
    bundled = Path(__file__).parent / 'models' / 'pose.onnx'
```

Inside `ensure_model`: Store the result in `bundled`: ((`Path(__file__).parent` divided by `'models'`) divided by `'pose.onnx'`). This is assignment, not an equality check.

### Line 26

```python
    target = bundled if bundled.exists() else data_folder() / 'pose.onnx'
```

Inside `ensure_model`: Store the result in `target`: `bundled` when `bundled.exists`: check whether this path currently exists. No arguments are supplied; otherwise (`data_folder`: get a writable folder for this user's models and sessions. No arguments are supplied divided by `'pose.onnx'`). This is assignment, not an equality check.

### Line 27

```python
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == MODEL_SHA256:
```

Inside `ensure_model`: Run the indented block only when this condition is true: `target.exists`: check whether this path currently exists. No arguments are supplied AND `hashlib.sha256(target.read_bytes()).hexdigest`: format the checksum as hexadecimal text. No arguments are supplied equals `MODEL_SHA256`. Other branches handle the remaining case.

### Line 28

```python
        return target
```

Inside `ensure_model`: End this function now and send back `target`. A bare return sends None.

### Line 29

```python
    temporary = target.with_suffix('.download')
```

Inside `ensure_model`: Store the result in `temporary`: `target.with_suffix`: make a related path with a different extension. Arguments: `'.download'`. This is assignment, not an equality check.

### Line 30

```python
    progress('Downloading the pose model. This only happens once.')
```

Inside `ensure_model`: Run this operation: `progress`: call this function with the supplied arguments. Arguments: `'Downloading the pose model. This only happens once.'`.

### Line 31

```python
    with urlopen(MODEL_URL, timeout=30) as response, open(temporary, 'wb') as output:
```

Inside `ensure_model`: Enter managed resources: `urlopen`: open an HTTP response with the supplied timeout. Arguments: `MODEL_URL`; timeout = `30` stored as `response`; `open`: open a file with the supplied mode and encoding. Arguments: `temporary`; `'wb'` stored as `output`. The resources are closed or restored when this block ends, including after errors.

### Line 32

```python
        while chunk := response.read(262144):
```

Inside `ensure_model`: Keep repeating the indented block while store `response.read`: read the next frame or next byte chunk from this resource. Arguments: `262144` in `chunk` and use that value as the condition. The body must advance or stop the loop.

### Line 33

```python
            if cancelled():
```

Inside `ensure_model`: Run the indented block only when this condition is true: `cancelled`: call this function with the supplied arguments. No arguments are supplied. Other branches handle the remaining case.

### Line 34

```python
                raise InterruptedError('Model download stopped.')
```

Inside `ensure_model`: Stop this operation by raising an exception: `InterruptedError`: call this function with the supplied arguments. Arguments: `'Model download stopped.'`. A matching except block can handle it.

### Line 35

```python
            output.write(chunk)
```

Inside `ensure_model`: Run this operation: `output.write`: write bytes or an encoded frame to the open output. Arguments: `chunk`.

### Line 36

```python
    if hashlib.sha256(temporary.read_bytes()).hexdigest() != MODEL_SHA256:
```

Inside `ensure_model`: Run the indented block only when this condition is true: `hashlib.sha256(temporary.read_bytes()).hexdigest`: format the checksum as hexadecimal text. No arguments are supplied does not equal `MODEL_SHA256`. Other branches handle the remaining case.

### Line 37

```python
        raise ValueError('The model download failed its checksum. Please try again.')
```

Inside `ensure_model`: Stop this operation by raising an exception: `ValueError`: call this function with the supplied arguments. Arguments: `'The model download failed its checksum. Please try again.'`. A matching except block can handle it.

### Line 38

```python
    temporary.replace(target)
```

Inside `ensure_model`: Run this operation: `temporary.replace`: replace the target path atomically on this filesystem, or replace matching text in a string. Arguments: `target`.

### Line 39

```python
    return target
```

Inside `ensure_model`: End this function now and send back `target`. A bare return sends None.

### Line 40

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 41

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 42

```python
class PoseDetector:
```

Define the `PoseDetector` class, inheriting from . Run a small pretrained pose model locally on the CPU.

### Line 43

```python
    """Run a small pretrained pose model locally on the CPU."""
```

Inside `PoseDetector`: Documentation string: Run a small pretrained pose model locally on the CPU. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 44

```python

```

Inside `PoseDetector`: Blank line. It separates related parts for readability and performs no operation.

### Line 45

```python
    def __init__(self, path):
```

Inside `PoseDetector`: Define `__init__(self, path)`. Its job: prepare the new object's state, controls, or runtime resources The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 46

```python
        options = ort.SessionOptions()
```

Inside `__init__`: Store the result in `options`: `ort.SessionOptions`: create options for the local model runtime. No arguments are supplied. This is assignment, not an equality check.

### Line 47

```python
        options.intra_op_num_threads = min(4, os.cpu_count() or 1)
```

Inside `__init__`: Store the result in `options.intra_op_num_threads`: `min`: choose the smallest value, or the item with the smallest key. Arguments: `4`; `os.cpu_count`: call this function with the supplied arguments. No arguments are supplied OR `1`. This is assignment, not an equality check.

### Line 48

```python
        self.session = ort.InferenceSession(str(path), sess_options=options, providers=['CPUExecutionProvider'])
```

Inside `__init__`: Store the result in `self.session`: `ort.InferenceSession`: load the ONNX model with the specified runtime options and CPU provider. Arguments: `str`: convert a value to text. Arguments: `path`; sess_options = `options`; providers = list containing `'CPUExecutionProvider'`. This is assignment, not an equality check.

### Line 49

```python
        self.input_name = self.session.get_inputs()[0].name
```

Inside `__init__`: Store the result in `self.input_name`: `self.session.get_inputs()[0].name`. This is assignment, not an equality check.

### Line 50

```python

```

Inside `PoseDetector`: Blank line. It separates related parts for readability and performs no operation.

### Line 51

```python
    def detect(self, frame, threshold=0.28, motion=None):
```

Inside `PoseDetector`: Define `detect(self, frame, threshold=0.28, motion=None)`. Its job: Search the full image and magnified moving regions, including rotated poses. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 52

```python
        """Search the full image and magnified moving regions, including rotated poses."""
```

Inside `detect`: Documentation string: Search the full image and magnified moving regions, including rotated poses. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 53

```python
        people = self.detect_upright(frame, threshold)
```

Inside `detect`: Store the result in `people`: `self.detect_upright`: prepare one image, run the model, and decode boxes and visible hip landmarks. Arguments: `frame`; `threshold`. This is assignment, not an equality check.

### Line 54

```python
        height, width = frame.shape[:2]
```

Inside `detect`: Store the result in `(height, width)`: `frame.shape[:2]`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 55

```python
        regions = motion_regions(motion, frame.shape) if motion else []
```

Inside `detect`: Store the result in `regions`: `motion_regions`: group strongly moving features and choose a magnified search region. Arguments: `motion`; `frame.shape` when `motion`; otherwise an empty list `[]`. This is assignment, not an equality check.

### Line 56

```python
        left, top = round(width * 0.2), round(height * 0.05)
```

Inside `detect`: Store the result in `(left, top)`: tuple containing `round`: round a number to the requested precision. Arguments: (`width` times `0.2`); `round`: round a number to the requested precision. Arguments: (`height` times `0.05`). Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 57

```python
        crop = frame[top:round(height * 0.95), left:round(width * 0.8)]
```

Inside `detect`: Store the result in `crop`: `frame[top:round(height * 0.95), left:round(width * 0.8)]`. This is assignment, not an equality check.

### Line 58

```python
        for person in self.detect_upright(crop, threshold) if not regions and motion is None else []:
```

Inside `detect`: Repeat the following indented block for each `person` from `self.detect_upright`: prepare one image, run the model, and decode boxes and visible hip landmarks. Arguments: `crop`; `threshold` when NOT `regions` AND `motion` is the same object as `None`; otherwise an empty list `[]`. Tuple targets unpack each loop item.

### Line 59

```python
            person['box'][0] += left
```

Inside `detect`: Update `person['box'][0]` using its old value plus `left`.

### Line 60

```python
            person['box'][1] += top
```

Inside `detect`: Update `person['box'][1]` using its old value plus `top`.

### Line 61

```python
            person['hip'] = [person['hip'][0] + left, person['hip'][1] + top]
```

Inside `detect`: Store the result in `person['hip']`: list containing (`person['hip'][0]` plus `left`); (`person['hip'][1]` plus `top`). This is assignment, not an equality check.

### Line 62

```python
            person['points'] = [[point[0] + left, point[1] + top, point[2]] for point in person['points']]
```

Inside `detect`: Store the result in `person['points']`: produce list containing (`point[0]` plus `left`); (`point[1]` plus `top`); `point[2]`, for each point in `person['points']`. This is assignment, not an equality check.

### Line 63

```python
            people.append(person)
```

Inside `detect`: Run this operation: `people.append`: add an item to the end of this list. Arguments: `person`.

### Line 64

```python
        for left, top, right, bottom in regions:
```

Inside `detect`: Repeat the following indented block for each `(left, top, right, bottom)` from `regions`. Tuple targets unpack each loop item.

### Line 65

```python
            region = frame[top:bottom, left:right]
```

Inside `detect`: Store the result in `region`: `frame[top:bottom, left:right]`. This is assignment, not an equality check.

### Line 66

```python
            region_height, region_width = region.shape[:2]
```

Inside `detect`: Store the result in `(region_height, region_width)`: `region.shape[:2]`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 67

```python
            for turn in (0, 1, 2, 3):
```

Inside `detect`: Repeat the following indented block for each `turn` from tuple containing `0`; `1`; `2`; `3`. Tuple targets unpack each loop item.

### Line 68

```python
                for person in self.detect_upright(np.rot90(region, turn).copy(), threshold):
```

Inside `detect`: Repeat the following indented block for each `person` from `self.detect_upright`: prepare one image, run the model, and decode boxes and visible hip landmarks. Arguments: `np.rot90(region, turn).copy`: make a separate copy so later drawing or changes do not overwrite the original. No arguments are supplied; `threshold`. Tuple targets unpack each loop item.

### Line 69

```python
                    self.restore_person(person, turn, region_width, region_height, left, top)
```

Inside `detect`: Run this operation: `self.restore_person`: reverse crop rotation and offset for boxes, hips, and body landmarks. Arguments: `person`; `turn`; `region_width`; `region_height`; `left`; `top`.

### Line 70

```python
                    people.append(person)
```

Inside `detect`: Run this operation: `people.append`: add an item to the end of this list. Arguments: `person`.

### Line 71

```python
        if not regions and motion is None:
```

Inside `detect`: Run the indented block only when this condition is true: NOT `regions` AND `motion` is the same object as `None`. Other branches handle the remaining case.

### Line 72

```python
            for turn in (1, 3):
```

Inside `detect`: Repeat the following indented block for each `turn` from tuple containing `1`; `3`. Tuple targets unpack each loop item.

### Line 73

```python
                for person in self.detect_upright(np.rot90(frame, turn).copy(), threshold):
```

Inside `detect`: Repeat the following indented block for each `person` from `self.detect_upright`: prepare one image, run the model, and decode boxes and visible hip landmarks. Arguments: `np.rot90(frame, turn).copy`: make a separate copy so later drawing or changes do not overwrite the original. No arguments are supplied; `threshold`. Tuple targets unpack each loop item.

### Line 74

```python
                    self.restore_person(person, turn, width, height)
```

Inside `detect`: Run this operation: `self.restore_person`: reverse crop rotation and offset for boxes, hips, and body landmarks. Arguments: `person`; `turn`; `width`; `height`.

### Line 75

```python
                    people.append(person)
```

Inside `detect`: Run this operation: `people.append`: add an item to the end of this list. Arguments: `person`.

### Line 76

```python
        keep = cv2.dnn.NMSBoxes([person['box'] for person in people], [person['score'] for person in people], threshold, 0.45)
```

Inside `detect`: Store the result in `keep`: `cv2.dnn.NMSBoxes`: discard strongly overlapping boxes while retaining stronger detections. Arguments: produce `person['box']`, for each person in `people`; produce `person['score']`, for each person in `people`; `threshold`; `0.45`. This is assignment, not an equality check.

### Line 77

```python
        return [people[index] for index in np.asarray(keep).reshape(-1)]
```

Inside `detect`: End this function now and send back produce `people[index]`, for each index in `np.asarray(keep).reshape`: change an array's dimensions without changing its values. Arguments: negative `1`. A bare return sends None.

### Line 78

```python

```

Inside `PoseDetector`: Blank line. It separates related parts for readability and performs no operation.

### Line 79

```python
    @staticmethod
```

Inside `PoseDetector`: Apply a decorator to the next method. `@staticmethod` calls this helper without supplying self or cls; all needed values are explicit parameters.

### Line 80

```python
    def restore_person(person, turn, width, height, left=0, top=0):
```

Inside `PoseDetector`: Define `restore_person(person, turn, width, height, left=0, top=0)`. Its job: Undo a crop rotation for every box corner and body landmark. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 81

```python
        """Undo a crop rotation for every box corner and body landmark."""
```

Inside `restore_person`: Documentation string: Undo a crop rotation for every box corner and body landmark. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 82

```python
        def restore(point):
```

Inside `restore_person`: Define `restore(point)`. Its job: undo a quarter-turn so detected coordinates refer to the original frame The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 83

```python
            x, y = point[:2]
```

Inside `restore`: Store the result in `(x, y)`: `point[:2]`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 84

```python
            if turn == 1:
```

Inside `restore`: Run the indented block only when this condition is true: `turn` equals `1`. Other branches handle the remaining case.

### Line 85

```python
                x, y = width - 1 - y, x
```

Inside `restore`: Store the result in `(x, y)`: tuple containing ((`width` minus `1`) minus `y`); `x`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 86

```python
            elif turn == 2:
```

Inside `restore`: If earlier branches did not run, test this additional condition: `turn == 2`.

### Line 87

```python
                x, y = width - 1 - x, height - 1 - y
```

Inside `restore`: Store the result in `(x, y)`: tuple containing ((`width` minus `1`) minus `x`); ((`height` minus `1`) minus `y`). Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 88

```python
            elif turn == 3:
```

Inside `restore`: If earlier branches did not run, test this additional condition: `turn == 3`.

### Line 89

```python
                x, y = y, height - 1 - x
```

Inside `restore`: Store the result in `(x, y)`: tuple containing `y`; ((`height` minus `1`) minus `x`). Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 90

```python
            return [float(x + left), float(y + top)]
```

Inside `restore`: End this function now and send back list containing `float`: convert a value to a decimal number. Arguments: (`x` plus `left`); `float`: convert a value to a decimal number. Arguments: (`y` plus `top`). A bare return sends None.

### Line 91

```python
        x, y, w, h = person['box']
```

Inside `restore_person`: Store the result in `(x, y, w, h)`: `person['box']`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 92

```python
        corners = np.array([restore([x, y]), restore([x + w, y + h])])
```

Inside `restore_person`: Store the result in `corners`: `np.array`: put the supplied values into a numerical array. Arguments: list containing `restore`: undo a quarter-turn so detected coordinates refer to the original frame. Arguments: list containing `x`; `y`; `restore`: undo a quarter-turn so detected coordinates refer to the original frame. Arguments: list containing (`x` plus `w`); (`y` plus `h`). This is assignment, not an equality check.

### Line 93

```python
        minimum, maximum = corners.min(axis=0), corners.max(axis=0)
```

Inside `restore_person`: Store the result in `(minimum, maximum)`: tuple containing `corners.min`: find the smallest array value along the specified axis. Arguments: axis = `0`; `corners.max`: find the largest array value along the specified axis. Arguments: axis = `0`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 94

```python
        person['box'] = [*minimum.tolist(), *(maximum - minimum).tolist()]
```

Inside `restore_person`: Store the result in `person['box']`: list containing `*minimum.tolist()`; `*(maximum - minimum).tolist()`. This is assignment, not an equality check.

### Line 95

```python
        person['hip'] = restore(person['hip'])
```

Inside `restore_person`: Store the result in `person['hip']`: `restore`: undo a quarter-turn so detected coordinates refer to the original frame. Arguments: `person['hip']`. This is assignment, not an equality check.

### Line 96

```python
        person['points'] = [restore(point) + [point[2]] for point in person['points']]
```

Inside `restore_person`: Store the result in `person['points']`: produce (`restore`: undo a quarter-turn so detected coordinates refer to the original frame. Arguments: `point` plus list containing `point[2]`), for each point in `person['points']`. This is assignment, not an equality check.

### Line 97

```python

```

Inside `PoseDetector`: Blank line. It separates related parts for readability and performs no operation.

### Line 98

```python
    def detect_upright(self, frame, threshold=0.28):
```

Inside `PoseDetector`: Define `detect_upright(self, frame, threshold=0.28)`. Its job: Return person boxes and 17 body landmarks in original image pixels. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 99

```python
        """Return person boxes and 17 body landmarks in original image pixels."""
```

Inside `detect_upright`: Documentation string: Return person boxes and 17 body landmarks in original image pixels. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 100

```python
        height, width = frame.shape[:2]
```

Inside `detect_upright`: Store the result in `(height, width)`: `frame.shape[:2]`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 101

```python
        ratio = min(640 / width, 640 / height)
```

Inside `detect_upright`: Store the result in `ratio`: `min`: choose the smallest value, or the item with the smallest key. Arguments: (`640` divided by `width`); (`640` divided by `height`). This is assignment, not an equality check.

### Line 102

```python
        resized = cv2.resize(frame, (round(width * ratio), round(height * ratio)))
```

Inside `detect_upright`: Store the result in `resized`: `cv2.resize`: resize an image to the requested width and height. Arguments: `frame`; tuple containing `round`: round a number to the requested precision. Arguments: (`width` times `ratio`); `round`: round a number to the requested precision. Arguments: (`height` times `ratio`). This is assignment, not an equality check.

### Line 103

```python
        left = (640 - resized.shape[1]) // 2
```

Inside `detect_upright`: Store the result in `left`: ((`640` minus `resized.shape[1]`) floor-divided by `2`). This is assignment, not an equality check.

### Line 104

```python
        top = (640 - resized.shape[0]) // 2
```

Inside `detect_upright`: Store the result in `top`: ((`640` minus `resized.shape[0]`) floor-divided by `2`). This is assignment, not an equality check.

### Line 105

```python
        padded = np.full((640, 640, 3), 114, dtype=np.uint8)
```

Inside `detect_upright`: Store the result in `padded`: `np.full`: create an array filled with a specified value. Arguments: tuple containing `640`; `640`; `3`; `114`; dtype = `np.uint8`. This is assignment, not an equality check.

### Line 106

```python
        padded[top:top + resized.shape[0], left:left + resized.shape[1]] = resized
```

Inside `detect_upright`: Store the result in `padded[top:top + resized.shape[0], left:left + resized.shape[1]]`: `resized`. This is assignment, not an equality check.

### Line 107

```python
        tensor = padded[:, :, ::-1].transpose(2, 0, 1)[None].astype(np.float32) / 255.0
```

Inside `detect_upright`: Take every pixel, reverse BGR channels into RGB, move the colour axis before height and width, add a batch dimension with `[None]`, convert to 32-bit floating point, and divide by 255. The resulting model input has shape `(1, 3, 640, 640)` and values from 0 to 1.

### Line 108

```python
        predictions = self.session.run(None, {self.input_name: tensor})[0][0].T
```

Inside `detect_upright`: Run the model using its actual input name. None asks for all outputs. The first [0] selects the output tensor, the second removes the one-image batch axis, and .T transposes the matrix. Rows now describe the 8400 possible detections; each row has 56 values.

### Line 109

```python
        predictions = predictions[predictions[:, 4] >= threshold]
```

Inside `detect_upright`: Column 4 is person confidence. Build a boolean mask for rows meeting the threshold and retain only those rows. The first four columns hold box centre X, centre Y, width, and height.

### Line 110

```python
        boxes, scores, poses = [], [], []
```

Inside `detect_upright`: Store the result in `(boxes, scores, poses)`: tuple containing an empty list `[]`; an empty list `[]`; an empty list `[]`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 111

```python
        for prediction in predictions:
```

Inside `detect_upright`: Repeat the following indented block for each `prediction` from `predictions`. Tuple targets unpack each loop item.

### Line 112

```python
            cx, cy, box_width, box_height = prediction[:4]
```

Inside `detect_upright`: Store the result in `(cx, cy, box_width, box_height)`: `prediction[:4]`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 113

```python
            box = [(cx - box_width / 2 - left) / ratio, (cy - box_height / 2 - top) / ratio, box_width / ratio, box_height / ratio]
```

Inside `detect_upright`: Store the result in `box`: list containing (((`cx` minus (`box_width` divided by `2`)) minus `left`) divided by `ratio`); (((`cy` minus (`box_height` divided by `2`)) minus `top`) divided by `ratio`); (`box_width` divided by `ratio`); (`box_height` divided by `ratio`). This is assignment, not an equality check.

### Line 114

```python
            points = prediction[5:].reshape(17, 3).copy()
```

Inside `detect_upright`: Skip the four box values and one person score. Reshape the remaining 51 values into 17 rows of X, Y, and landmark score. Copy them before converting coordinates so the prediction buffer is not changed.

### Line 115

```python
            points[:, 0] = (points[:, 0] - left) / ratio
```

Inside `detect_upright`: Store the result in `points[:, 0]`: ((`points[:, 0]` minus `left`) divided by `ratio`). This is assignment, not an equality check.

### Line 116

```python
            points[:, 1] = (points[:, 1] - top) / ratio
```

Inside `detect_upright`: Store the result in `points[:, 1]`: ((`points[:, 1]` minus `top`) divided by `ratio`). This is assignment, not an equality check.

### Line 117

```python
            if box[2] < 12 or box[3] < 16:
```

Inside `detect_upright`: Run the indented block only when this condition is true: `box[2]` is less than `12` OR `box[3]` is less than `16`. Other branches handle the remaining case.

### Line 118

```python
                continue
```

Inside `detect_upright`: Skip the rest of this loop iteration and try the next item. This rejects the current unsuitable detection, fit, or sample.

### Line 119

```python
            boxes.append(list(map(float, box)))
```

Inside `detect_upright`: Run this operation: `boxes.append`: add an item to the end of this list. Arguments: `list`: create a list from the supplied values. Arguments: `map`: apply the first function to each supplied value. Arguments: `float`; `box`.

### Line 120

```python
            scores.append(float(prediction[4]))
```

Inside `detect_upright`: Run this operation: `scores.append`: add an item to the end of this list. Arguments: `float`: convert a value to a decimal number. Arguments: `prediction[4]`.

### Line 121

```python
            poses.append(points)
```

Inside `detect_upright`: Run this operation: `poses.append`: add an item to the end of this list. Arguments: `points`.

### Line 122

```python
        keep = cv2.dnn.NMSBoxes(boxes, scores, threshold, 0.45)
```

Inside `detect_upright`: Store the result in `keep`: `cv2.dnn.NMSBoxes`: discard strongly overlapping boxes while retaining stronger detections. Arguments: `boxes`; `scores`; `threshold`; `0.45`. This is assignment, not an equality check.

### Line 123

```python
        people = []
```

Inside `detect_upright`: Store the result in `people`: an empty list `[]`. This is assignment, not an equality check.

### Line 124

```python
        for index in np.asarray(keep).reshape(-1):
```

Inside `detect_upright`: Repeat the following indented block for each `index` from `np.asarray(keep).reshape`: change an array's dimensions without changing its values. Arguments: negative `1`. Tuple targets unpack each loop item.

### Line 125

```python
            points = poses[index]
```

Inside `detect_upright`: Store the result in `points`: `poses[index]`. This is assignment, not an equality check.

### Line 126

```python
            hips = points[[11, 12]]
```

Inside `detect_upright`: Select zero-based landmark rows 11 and 12, the model's left and right hip. These two estimated points are the requested hip proxy.

### Line 127

```python
            visible = hips[:, 2] >= 0.30
```

Inside `detect_upright`: Store the result in `visible`: `hips[:, 2]` is at least `0.3`. This is assignment, not an equality check.

### Line 128

```python
            if not visible.any():
```

Inside `detect_upright`: Run the indented block only when this condition is true: NOT `visible.any`: check whether at least one array condition is true. No arguments are supplied. Other branches handle the remaining case.

### Line 129

```python
                continue
```

Inside `detect_upright`: Skip the rest of this loop iteration and try the next item. This rejects the current unsuitable detection, fit, or sample.

### Line 130

```python
            hip = np.average(hips[visible, :2], axis=0, weights=hips[visible, 2])
```

Inside `detect_upright`: Store the result in `hip`: `np.average`: calculate an average, optionally weighting stronger hip evidence more heavily. Arguments: `hips[visible, :2]`; axis = `0`; weights = `hips[visible, 2]`. This is assignment, not an equality check.

### Line 131

```python
            if not (0 <= hip[0] < width and 0 <= hip[1] < height):
```

Inside `detect_upright`: Run the indented block only when this condition is true: NOT `0` is at most `hip[0]` and is less than `width` AND `0` is at most `hip[1]` and is less than `height`. Other branches handle the remaining case.

### Line 132

```python
                continue
```

Inside `detect_upright`: Skip the rest of this loop iteration and try the next item. This rejects the current unsuitable detection, fit, or sample.

### Line 133

```python
            people.append(dict(box=boxes[index], hip=hip.tolist(), score=scores[index], hip_score=float(hips[visible, 2].mean()), points=points.tolist()))
```

Inside `detect_upright`: Run this operation: `people.append`: add an item to the end of this list. Arguments: `dict`: create a dictionary from the named fields. Arguments: box = `boxes[index]`; hip = `hip.tolist`: convert numerical arrays to ordinary Python lists for JSON storage. No arguments are supplied; score = `scores[index]`; hip_score = `float`: convert a value to a decimal number. Arguments: `hips[visible, 2].mean`: calculate the arithmetic mean of array values. No arguments are supplied; points = `points.tolist`: convert numerical arrays to ordinary Python lists for JSON storage. No arguments are supplied.

### Line 134

```python
        return people
```

Inside `detect_upright`: End this function now and send back `people`. A bare return sends None.

### Line 135

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 136

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 137

```python
def choose_athlete(people, frame_shape, previous=None):
```

Define `choose_athlete(people, frame_shape, previous=None)`. Its job: Prefer a central prominent person, then favour continuity across frames. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 138

```python
    """Prefer a central prominent person, then favour continuity across frames."""
```

Inside `choose_athlete`: Documentation string: Prefer a central prominent person, then favour continuity across frames. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 139

```python
    if not people:
```

Inside `choose_athlete`: Run the indented block only when this condition is true: NOT `people`. Other branches handle the remaining case.

### Line 140

```python
        return None
```

Inside `choose_athlete`: End this function now and send back `None`. A bare return sends None.

### Line 141

```python
    height, width = frame_shape[:2]
```

Inside `choose_athlete`: Store the result in `(height, width)`: `frame_shape[:2]`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 142

```python
    ranked = []
```

Inside `choose_athlete`: Store the result in `ranked`: an empty list `[]`. This is assignment, not an equality check.

### Line 143

```python
    for person in people:
```

Inside `choose_athlete`: Repeat the following indented block for each `person` from `people`. Tuple targets unpack each loop item.

### Line 144

```python
        x, y, box_width, box_height = person['box']
```

Inside `choose_athlete`: Store the result in `(x, y, box_width, box_height)`: `person['box']`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 145

```python
        central = 1 - min(1, abs(person['hip'][0] / width - 0.5) * 1.5)
```

Inside `choose_athlete`: Store the result in `central`: (`1` minus `min`: choose the smallest value, or the item with the smallest key. Arguments: `1`; (`abs`: call this function with the supplied arguments. Arguments: ((`person['hip'][0]` divided by `width`) minus `0.5`) times `1.5`)). This is assignment, not an equality check.

### Line 146

```python
        prominence = min(1, box_width * box_height / (width * height) * 12)
```

Inside `choose_athlete`: Store the result in `prominence`: `min`: choose the smallest value, or the item with the smallest key. Arguments: `1`; (((`box_width` times `box_height`) divided by (`width` times `height`)) times `12`). This is assignment, not an equality check.

### Line 147

```python
        rank = person['score'] * 0.20 + central * 0.30 + prominence * 0.15 + person.get('motion', 0) * 0.65
```

Inside `choose_athlete`: Store the result in `rank`: ((((`person['score']` times `0.2`) plus (`central` times `0.3`)) plus (`prominence` times `0.15`)) plus (`person.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'motion'`; `0` times `0.65`)). This is assignment, not an equality check.

### Line 148

```python
        if previous is not None:
```

Inside `choose_athlete`: Run the indented block only when this condition is true: `previous` is not the same object as `None`. Other branches handle the remaining case.

### Line 149

```python
            distance = np.linalg.norm((np.array(person['hip']) - previous['hip']) / [width, height])
```

Inside `choose_athlete`: Store the result in `distance`: `np.linalg.norm`: calculate the length of a displacement vector. Arguments: ((`np.array`: put the supplied values into a numerical array. Arguments: `person['hip']` minus `previous['hip']`) divided by list containing `width`; `height`). This is assignment, not an equality check.

### Line 150

```python
            rank += max(0, 0.25 - distance)
```

Inside `choose_athlete`: Update `rank` using its old value plus `max`: choose the largest value, or the item with the largest key. Arguments: `0`; (`0.25` minus `distance`).

### Line 151

```python
        ranked.append((rank, person))
```

Inside `choose_athlete`: Run this operation: `ranked.append`: add an item to the end of this list. Arguments: tuple containing `rank`; `person`.

### Line 152

```python
    ranked.sort(key=lambda item: item[0], reverse=True)
```

Inside `choose_athlete`: Run this operation: `ranked.sort`: reorder this list in place using the supplied key. Arguments: key = a short function taking `item` and returning `item[0]`; reverse = `True`.

### Line 153

```python
    best = dict(ranked[0][1])
```

Inside `choose_athlete`: Store the result in `best`: `dict`: create a dictionary from the named fields. Arguments: `ranked[0][1]`. This is assignment, not an equality check.

### Line 154

```python
    best['ambiguous'] = bool(len(ranked) > 1 and ranked[0][0] - ranked[1][0] < 0.10)
```

Inside `choose_athlete`: Store the result in `best['ambiguous']`: `bool`: convert a condition to a plain Python True or False. Arguments: `len`: count items. Arguments: `ranked` is greater than `1` AND (`ranked[0][0]` minus `ranked[1][0]`) is less than `0.1`. This is assignment, not an equality check.

### Line 155

```python
    return best
```

Inside `choose_athlete`: End this function now and send back `best`. A bare return sends None.

### Line 156

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 157

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 158

```python
def motion_field(previous_frame, frame):
```

Define `motion_field(previous_frame, frame)`. Its job: Remove camera pan and zoom from tracked feature movement. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 159

```python
    """Remove camera pan and zoom from tracked feature movement."""
```

Inside `motion_field`: Documentation string: Remove camera pan and zoom from tracked feature movement. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 160

```python
    if previous_frame is None or previous_frame.shape != frame.shape:
```

Inside `motion_field`: Run the indented block only when this condition is true: `previous_frame` is the same object as `None` OR `previous_frame.shape` does not equal `frame.shape`. Other branches handle the remaining case.

### Line 161

```python
        return None
```

Inside `motion_field`: End this function now and send back `None`. A bare return sends None.

### Line 162

```python
    ratio = min(1, 640 / frame.shape[1])
```

Inside `motion_field`: Store the result in `ratio`: `min`: choose the smallest value, or the item with the smallest key. Arguments: `1`; (`640` divided by `frame.shape[1]`). This is assignment, not an equality check.

### Line 163

```python
    size = (round(frame.shape[1] * ratio), round(frame.shape[0] * ratio))
```

Inside `motion_field`: Store the result in `size`: tuple containing `round`: round a number to the requested precision. Arguments: (`frame.shape[1]` times `ratio`); `round`: round a number to the requested precision. Arguments: (`frame.shape[0]` times `ratio`). This is assignment, not an equality check.

### Line 164

```python
    before = cv2.resize(cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY), size)
```

Inside `motion_field`: Store the result in `before`: `cv2.resize`: resize an image to the requested width and height. Arguments: `cv2.cvtColor`: convert between colour representations. Arguments: `previous_frame`; `cv2.COLOR_BGR2GRAY`; `size`. This is assignment, not an equality check.

### Line 165

```python
    after = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), size)
```

Inside `motion_field`: Store the result in `after`: `cv2.resize`: resize an image to the requested width and height. Arguments: `cv2.cvtColor`: convert between colour representations. Arguments: `frame`; `cv2.COLOR_BGR2GRAY`; `size`. This is assignment, not an equality check.

### Line 166

```python
    points = cv2.goodFeaturesToTrack(before, 800, 0.01, 5)
```

Inside `motion_field`: Store the result in `points`: `cv2.goodFeaturesToTrack`: find strong image corners suitable for following background and person movement. Arguments: `before`; `800`; `0.01`; `5`. This is assignment, not an equality check.

### Line 167

```python
    if points is None or len(points) < 12:
```

Inside `motion_field`: Run the indented block only when this condition is true: `points` is the same object as `None` OR `len`: count items. Arguments: `points` is less than `12`. Other branches handle the remaining case.

### Line 168

```python
        return None
```

Inside `motion_field`: End this function now and send back `None`. A bare return sends None.

### Line 169

```python
    moved, status, errors = cv2.calcOpticalFlowPyrLK(before, after, points, None)
```

Inside `motion_field`: Store the result in `(moved, status, errors)`: `cv2.calcOpticalFlowPyrLK`: track corner positions between images with pyramidal Lucas-Kanade optical flow. Arguments: `before`; `after`; `points`; `None`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 170

```python
    if moved is None:
```

Inside `motion_field`: Run the indented block only when this condition is true: `moved` is the same object as `None`. Other branches handle the remaining case.

### Line 171

```python
        return None
```

Inside `motion_field`: End this function now and send back `None`. A bare return sends None.

### Line 172

```python
    valid = status.reshape(-1) == 1
```

Inside `motion_field`: Store the result in `valid`: `status.reshape`: change an array's dimensions without changing its values. Arguments: negative `1` equals `1`. This is assignment, not an equality check.

### Line 173

```python
    old, new = points.reshape(-1, 2)[valid], moved.reshape(-1, 2)[valid]
```

Inside `motion_field`: Store the result in `(old, new)`: tuple containing `points.reshape(-1, 2)[valid]`; `moved.reshape(-1, 2)[valid]`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 174

```python
    if len(old) < 12:
```

Inside `motion_field`: Run the indented block only when this condition is true: `len`: count items. Arguments: `old` is less than `12`. Other branches handle the remaining case.

### Line 175

```python
        return None
```

Inside `motion_field`: End this function now and send back `None`. A bare return sends None.

### Line 176

```python
    transform, inliers = cv2.estimateAffinePartial2D(old, new, method=cv2.RANSAC, ransacReprojThreshold=3)
```

Inside `motion_field`: Store the result in `(transform, inliers)`: `cv2.estimateAffinePartial2D`: robustly estimate global translation, rotation, and scale from matched image features. Arguments: `old`; `new`; method = `cv2.RANSAC`; ransacReprojThreshold = `3`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 177

```python
    if transform is None:
```

Inside `motion_field`: Run the indented block only when this condition is true: `transform` is the same object as `None`. Other branches handle the remaining case.

### Line 178

```python
        return None
```

Inside `motion_field`: End this function now and send back `None`. A bare return sends None.

### Line 179

```python
    predicted = old @ transform[:, :2].T + transform[:, 2]
```

Inside `motion_field`: Store the result in `predicted`: ((`old` matrix multiplied by `transform[:, :2].T`) plus `transform[:, 2]`). This is assignment, not an equality check.

### Line 180

```python
    residual = np.linalg.norm(new - predicted, axis=1)
```

Inside `motion_field`: Store the result in `residual`: `np.linalg.norm`: calculate the length of a displacement vector. Arguments: (`new` minus `predicted`); axis = `1`. This is assignment, not an equality check.

### Line 181

```python
    baseline = float(np.median(residual))
```

Inside `motion_field`: Store the result in `baseline`: `float`: convert a value to a decimal number. Arguments: `np.median`: take the middle value after sorting, reducing the effect of one extreme value. Arguments: `residual`. This is assignment, not an equality check.

### Line 182

```python
    return dict(points=new, residual=residual, baseline=baseline, ratio=ratio, size=size)
```

Inside `motion_field`: End this function now and send back `dict`: create a dictionary from the named fields. Arguments: points = `new`; residual = `residual`; baseline = `baseline`; ratio = `ratio`; size = `size`. A bare return sends None.

### Line 183

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 184

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 185

```python
def motion_regions(field, frame_shape):
```

Define `motion_regions(field, frame_shape)`. Its job: Magnify the strongest moving cluster so a small airborne rider can be found. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 186

```python
    """Magnify the strongest moving cluster so a small airborne rider can be found."""
```

Inside `motion_regions`: Documentation string: Magnify the strongest moving cluster so a small airborne rider can be found. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 187

```python
    width, height = field['size']
```

Inside `motion_regions`: Store the result in `(width, height)`: `field['size']`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 188

```python
    points, residual = field['points'], field['residual']
```

Inside `motion_regions`: Store the result in `(points, residual)`: tuple containing `field['points']`; `field['residual']`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 189

```python
    moving = residual > max(3, field['baseline'] * 3)
```

Inside `motion_regions`: Store the result in `moving`: `residual` is greater than `max`: choose the largest value, or the item with the largest key. Arguments: `3`; (`field['baseline']` times `3`). This is assignment, not an equality check.

### Line 190

```python
    mask = np.zeros((height, width), dtype=np.uint8)
```

Inside `motion_regions`: Store the result in `mask`: `np.zeros`: create an array filled with zeros, here an initially empty mask. Arguments: tuple containing `height`; `width`; dtype = `np.uint8`. This is assignment, not an equality check.

### Line 191

```python
    for point in points[moving]:
```

Inside `motion_regions`: Repeat the following indented block for each `point` from `points[moving]`. Tuple targets unpack each loop item.

### Line 192

```python
        cv2.circle(mask, tuple(np.rint(point).astype(int)), 12, 255, -1)
```

Inside `motion_regions`: Run this operation: `cv2.circle`: draw a point marker on the supplied image. Arguments: `mask`; `tuple`: create a tuple from the supplied values. Arguments: `np.rint(point).astype`: convert array values to the requested numeric type. Arguments: `int`; `12`; `255`; negative `1`.

### Line 193

```python
    count, labels, stats, centres = cv2.connectedComponentsWithStats(mask)
```

Inside `motion_regions`: Store the result in `(count, labels, stats, centres)`: `cv2.connectedComponentsWithStats`: label touching mask regions and measure their sizes and bounds. Arguments: `mask`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 194

```python
    ranked = []
```

Inside `motion_regions`: Store the result in `ranked`: an empty list `[]`. This is assignment, not an equality check.

### Line 195

```python
    for x, y, w, h, area in stats[1:]:
```

Inside `motion_regions`: Repeat the following indented block for each `(x, y, w, h, area)` from `stats[1:]`. Tuple targets unpack each loop item.

### Line 196

```python
        inside = moving & (points[:, 0] >= x) & (points[:, 0] <= x + w) & (points[:, 1] >= y) & (points[:, 1] <= y + h)
```

Inside `motion_regions`: Store the result in `inside`: ((((`moving` element by element AND `points[:, 0]` is at least `x`) element by element AND `points[:, 0]` is at most (`x` plus `w`)) element by element AND `points[:, 1]` is at least `y`) element by element AND `points[:, 1]` is at most (`y` plus `h`)). This is assignment, not an equality check.

### Line 197

```python
        if inside.sum() < 5 or w * h > width * height * 0.4:
```

Inside `motion_regions`: Run the indented block only when this condition is true: `inside.sum`: count true support pixels or add numeric array values. No arguments are supplied is less than `5` OR (`w` times `h`) is greater than ((`width` times `height`) times `0.4`). Other branches handle the remaining case.

### Line 198

```python
            continue
```

Inside `motion_regions`: Skip the rest of this loop iteration and try the next item. This rejects the current unsuitable detection, fit, or sample.

### Line 199

```python
        centre = points[inside].mean(axis=0) / field['ratio']
```

Inside `motion_regions`: Store the result in `centre`: (`points[inside].mean`: calculate the arithmetic mean of array values. Arguments: axis = `0` divided by `field['ratio']`). This is assignment, not an equality check.

### Line 200

```python
        if not frame_shape[1] * 0.15 < centre[0] < frame_shape[1] * 0.85:
```

Inside `motion_regions`: Run the indented block only when this condition is true: NOT (`frame_shape[1]` times `0.15`) is less than `centre[0]` and is less than (`frame_shape[1]` times `0.85`). Other branches handle the remaining case.

### Line 201

```python
            continue
```

Inside `motion_regions`: Skip the rest of this loop iteration and try the next item. This rejects the current unsuitable detection, fit, or sample.

### Line 202

```python
        side = max(200 * frame_shape[1] / 960, max(w, h) / field['ratio'] * 1.1)
```

Inside `motion_regions`: Store the result in `side`: `max`: choose the largest value, or the item with the largest key. Arguments: ((`200` times `frame_shape[1]`) divided by `960`); ((`max`: choose the largest value, or the item with the largest key. Arguments: `w`; `h` divided by `field['ratio']`) times `1.1`). This is assignment, not an equality check.

### Line 203

```python
        left, top = np.maximum([0, 0], centre - side / 2).astype(int)
```

Inside `motion_regions`: Store the result in `(left, top)`: `np.maximum([0, 0], centre - side / 2).astype`: convert array values to the requested numeric type. Arguments: `int`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 204

```python
        right, bottom = np.minimum([frame_shape[1], frame_shape[0]], centre + side / 2).astype(int)
```

Inside `motion_regions`: Store the result in `(right, bottom)`: `np.minimum([frame_shape[1], frame_shape[0]], centre + side / 2).astype`: convert array values to the requested numeric type. Arguments: `int`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 205

```python
        ranked.append((float(residual[inside].sum()), [left, top, right, bottom]))
```

Inside `motion_regions`: Run this operation: `ranked.append`: add an item to the end of this list. Arguments: tuple containing `float`: convert a value to a decimal number. Arguments: `residual[inside].sum`: count true support pixels or add numeric array values. No arguments are supplied; list containing `left`; `top`; `right`; `bottom`.

### Line 206

```python
    ranked.sort(key=lambda item: item[0], reverse=True)
```

Inside `motion_regions`: Run this operation: `ranked.sort`: reorder this list in place using the supplied key. Arguments: key = a short function taking `item` and returning `item[0]`; reverse = `True`.

### Line 207

```python
    return [item[1] for item in ranked[:1]]
```

Inside `motion_regions`: End this function now and send back produce `item[1]`, for each item in `ranked[:1]`. A bare return sends None.

### Line 208

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 209

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 210

```python
def score_motion(previous_frame, frame, people, field=None):
```

Define `score_motion(previous_frame, frame, people, field=None)`. Its job: Score each person against the same camera compensated feature field. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 211

```python
    """Score each person against the same camera compensated feature field."""
```

Inside `score_motion`: Documentation string: Score each person against the same camera compensated feature field. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 212

```python
    field = field if field is not None else motion_field(previous_frame, frame)
```

Inside `score_motion`: Store the result in `field`: `field` when `field` is not the same object as `None`; otherwise `motion_field`: track image corners and remove common camera pan, rotation, and zoom. Arguments: `previous_frame`; `frame`. This is assignment, not an equality check.

### Line 213

```python
    if field is None:
```

Inside `score_motion`: Run the indented block only when this condition is true: `field` is the same object as `None`. Other branches handle the remaining case.

### Line 214

```python
        return
```

Inside `score_motion`: End this function now and send back no explicit value. A bare return sends None.

### Line 215

```python
    new, residual, baseline = field['points'], field['residual'], field['baseline']
```

Inside `score_motion`: Store the result in `(new, residual, baseline)`: tuple containing `field['points']`; `field['residual']`; `field['baseline']`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 216

```python
    for person in people:
```

Inside `score_motion`: Repeat the following indented block for each `person` from `people`. Tuple targets unpack each loop item.

### Line 217

```python
        x, y, w, h = np.array(person['box']) * field['ratio']
```

Inside `score_motion`: Store the result in `(x, y, w, h)`: (`np.array`: put the supplied values into a numerical array. Arguments: `person['box']` times `field['ratio']`). Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 218

```python
        inside = (new[:, 0] >= x) & (new[:, 0] <= x + w) & (new[:, 1] >= y) & (new[:, 1] <= y + h)
```

Inside `score_motion`: Store the result in `inside`: (((`new[:, 0]` is at least `x` element by element AND `new[:, 0]` is at most (`x` plus `w`)) element by element AND `new[:, 1]` is at least `y`) element by element AND `new[:, 1]` is at most (`y` plus `h`)). This is assignment, not an equality check.

### Line 219

```python
        if inside.sum() >= 3:
```

Inside `score_motion`: Run the indented block only when this condition is true: `inside.sum`: count true support pixels or add numeric array values. No arguments are supplied is at least `3`. Other branches handle the remaining case.

### Line 220

```python
            motion = max(0, float(np.percentile(residual[inside], 70)) - baseline)
```

Inside `score_motion`: Store the result in `motion`: `max`: choose the largest value, or the item with the largest key. Arguments: `0`; (`float`: convert a value to a decimal number. Arguments: `np.percentile`: find a percentile for a robust chart display scale. Arguments: `residual[inside]`; `70` minus `baseline`). This is assignment, not an equality check.

### Line 221

```python
            person['motion'] = min(1, motion / max(2, field['size'][1] * 0.025))
```

Inside `score_motion`: Store the result in `person['motion']`: `min`: choose the smallest value, or the item with the smallest key. Arguments: `1`; (`motion` divided by `max`: choose the largest value, or the item with the largest key. Arguments: `2`; (`field['size'][1]` times `0.025`)). This is assignment, not an equality check.

### Line 222

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 223

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 224

```python
def find_lip(frame, hip, box):
```

Define `find_lip(frame, hip, box)`. Its job: Fit the top local blue boundary and reject sparse or unstable fits. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 225

```python
    """Fit the top local blue boundary and reject sparse or unstable fits."""
```

Inside `find_lip`: Documentation string: Fit the top local blue boundary and reject sparse or unstable fits. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 226

```python
    height, width = frame.shape[:2]
```

Inside `find_lip`: Store the result in `(height, width)`: `frame.shape[:2]`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 227

```python
    small = cv2.resize(frame, (min(960, width), round(height * min(960, width) / width)))
```

Inside `find_lip`: Store the result in `small`: `cv2.resize`: resize an image to the requested width and height. Arguments: `frame`; tuple containing `min`: choose the smallest value, or the item with the smallest key. Arguments: `960`; `width`; `round`: round a number to the requested precision. Arguments: ((`height` times `min`: choose the smallest value, or the item with the smallest key. Arguments: `960`; `width`) divided by `width`). This is assignment, not an equality check.

### Line 228

```python
    ratio = small.shape[1] / width
```

Inside `find_lip`: Store the result in `ratio`: (`small.shape[1]` divided by `width`). This is assignment, not an equality check.

### Line 229

```python
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
```

Inside `find_lip`: Store the result in `hsv`: `cv2.cvtColor`: convert between colour representations. Arguments: `small`; `cv2.COLOR_BGR2HSV`. This is assignment, not an equality check.

### Line 230

```python
    mask = cv2.inRange(hsv, (80, 35, 60), (118, 255, 255))
```

Inside `find_lip`: Store the result in `mask`: `cv2.inRange`: make a mask whose white pixels fall inside the lower and upper colour limits. Arguments: `hsv`; tuple containing `80`; `35`; `60`; tuple containing `118`; `255`; `255`. This is assignment, not an equality check.

### Line 231

```python
    count, labels, stats, centres = cv2.connectedComponentsWithStats(mask)
```

Inside `find_lip`: Store the result in `(count, labels, stats, centres)`: `cv2.connectedComponentsWithStats`: label touching mask regions and measure their sizes and bounds. Arguments: `mask`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 232

```python
    clean = np.zeros_like(mask)
```

Inside `find_lip`: Store the result in `clean`: `np.zeros_like`: call this function with the supplied arguments. Arguments: `mask`. This is assignment, not an equality check.

### Line 233

```python
    for component in range(1, count):
```

Inside `find_lip`: Repeat the following indented block for each `component` from `range`: produce integer loop positions, excluding the upper bound. Arguments: `1`; `count`. Tuple targets unpack each loop item.

### Line 234

```python
        x, y, w, h, area = stats[component]
```

Inside `find_lip`: Store the result in `(x, y, w, h, area)`: `stats[component]`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 235

```python
        if w >= 15 and area >= 25:
```

Inside `find_lip`: Run the indented block only when this condition is true: `w` is at least `15` AND `area` is at least `25`. Other branches handle the remaining case.

### Line 236

```python
            clean[labels == component] = 255
```

Inside `find_lip`: Store the result in `clean[labels == component]`: `255`. This is assignment, not an equality check.

### Line 237

```python
    hip_x, hip_y = np.array(hip) * ratio
```

Inside `find_lip`: Store the result in `(hip_x, hip_y)`: (`np.array`: put the supplied values into a numerical array. Arguments: `hip` times `ratio`). Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 238

```python
    radius = max(65, min(240, box[2] * ratio * 1.8))
```

Inside `find_lip`: Store the result in `radius`: `max`: choose the largest value, or the item with the largest key. Arguments: `65`; `min`: choose the smallest value, or the item with the smallest key. Arguments: `240`; ((`box[2]` times `ratio`) times `1.8`). This is assignment, not an equality check.

### Line 239

```python
    first = max(0, int(hip_x - radius))
```

Inside `find_lip`: Store the result in `first`: `max`: choose the largest value, or the item with the largest key. Arguments: `0`; `int`: convert a value to a whole number. Arguments: (`hip_x` minus `radius`). This is assignment, not an equality check.

### Line 240

```python
    last = min(small.shape[1], int(hip_x + radius))
```

Inside `find_lip`: Store the result in `last`: `min`: choose the smallest value, or the item with the smallest key. Arguments: `small.shape[1]`; `int`: convert a value to a whole number. Arguments: (`hip_x` plus `radius`). This is assignment, not an equality check.

### Line 241

```python
    xs, ys = [], []
```

Inside `find_lip`: Store the result in `(xs, ys)`: tuple containing an empty list `[]`; an empty list `[]`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 242

```python
    for x in range(first, last, 2):
```

Inside `find_lip`: Repeat the following indented block for each `x` from `range`: produce integer loop positions, excluding the upper bound. Arguments: `first`; `last`; `2`. Tuple targets unpack each loop item.

### Line 243

```python
        pixels = np.flatnonzero(clean[:, x])
```

Inside `find_lip`: Store the result in `pixels`: `np.flatnonzero`: return positions at which an array is nonzero or true. Arguments: `clean[:, x]`. This is assignment, not an equality check.

### Line 244

```python
        if len(pixels):
```

Inside `find_lip`: Run the indented block only when this condition is true: `len`: count items. Arguments: `pixels`. Other branches handle the remaining case.

### Line 245

```python
            xs.append(x)
```

Inside `find_lip`: Run this operation: `xs.append`: add an item to the end of this list. Arguments: `x`.

### Line 246

```python
            ys.append(float(pixels[0]))
```

Inside `find_lip`: Run this operation: `ys.append`: add an item to the end of this list. Arguments: `float`: convert a value to a decimal number. Arguments: `pixels[0]`.

### Line 247

```python
    if len(xs) < 12:
```

Inside `find_lip`: Run the indented block only when this condition is true: `len`: count items. Arguments: `xs` is less than `12`. Other branches handle the remaining case.

### Line 248

```python
        return None
```

Inside `find_lip`: End this function now and send back `None`. A bare return sends None.

### Line 249

```python
    xs, ys = np.array(xs, dtype=float), np.array(ys, dtype=float)
```

Inside `find_lip`: Store the result in `(xs, ys)`: tuple containing `np.array`: put the supplied values into a numerical array. Arguments: `xs`; dtype = `float`; `np.array`: put the supplied values into a numerical array. Arguments: `ys`; dtype = `float`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 250

```python
    best = None
```

Inside `find_lip`: Store the result in `best`: `None`. This is assignment, not an equality check.

### Line 251

```python
    rng = np.random.default_rng(7)
```

Inside `find_lip`: Store the result in `rng`: `np.random.default_rng`: create a repeatable random generator from the given seed. Arguments: `7`. This is assignment, not an equality check.

### Line 252

```python
    for _ in range(80):
```

Inside `find_lip`: Repeat the following indented block for each `_` from `range`: produce integer loop positions, excluding the upper bound. Arguments: `80`. Tuple targets unpack each loop item.

### Line 253

```python
        pair = rng.choice(len(xs), 2, replace=False)
```

Inside `find_lip`: Store the result in `pair`: `rng.choice`: select random distinct support positions for a trial line. Arguments: `len`: count items. Arguments: `xs`; `2`; replace = `False`. This is assignment, not an equality check.

### Line 254

```python
        if abs(xs[pair[1]] - xs[pair[0]]) < radius * 0.35:
```

Inside `find_lip`: Run the indented block only when this condition is true: `abs`: call this function with the supplied arguments. Arguments: (`xs[pair[1]]` minus `xs[pair[0]]`) is less than (`radius` times `0.35`). Other branches handle the remaining case.

### Line 255

```python
            continue
```

Inside `find_lip`: Skip the rest of this loop iteration and try the next item. This rejects the current unsuitable detection, fit, or sample.

### Line 256

```python
        slope = (ys[pair[1]] - ys[pair[0]]) / (xs[pair[1]] - xs[pair[0]])
```

Inside `find_lip`: Store the result in `slope`: ((`ys[pair[1]]` minus `ys[pair[0]]`) divided by (`xs[pair[1]]` minus `xs[pair[0]]`)). This is assignment, not an equality check.

### Line 257

```python
        intercept = ys[pair[0]] - slope * xs[pair[0]]
```

Inside `find_lip`: Store the result in `intercept`: (`ys[pair[0]]` minus (`slope` times `xs[pair[0]]`)). This is assignment, not an equality check.

### Line 258

```python
        errors = np.abs(ys - (slope * xs + intercept))
```

Inside `find_lip`: Store the result in `errors`: `np.abs`: take absolute values element by element. Arguments: (`ys` minus ((`slope` times `xs`) plus `intercept`)). This is assignment, not an equality check.

### Line 259

```python
        inliers = errors < max(5, small.shape[0] * 0.012)
```

Inside `find_lip`: Store the result in `inliers`: `errors` is less than `max`: choose the largest value, or the item with the largest key. Arguments: `5`; (`small.shape[0]` times `0.012`). This is assignment, not an equality check.

### Line 260

```python
        support = int(inliers.sum())
```

Inside `find_lip`: Store the result in `support`: `int`: convert a value to a whole number. Arguments: `inliers.sum`: count true support pixels or add numeric array values. No arguments are supplied. This is assignment, not an equality check.

### Line 261

```python
        if best is None or support > best[0]:
```

Inside `find_lip`: Run the indented block only when this condition is true: `best` is the same object as `None` OR `support` is greater than `best[0]`. Other branches handle the remaining case.

### Line 262

```python
            best = (support, inliers)
```

Inside `find_lip`: Store the result in `best`: tuple containing `support`; `inliers`. This is assignment, not an equality check.

### Line 263

```python
    if best is None or best[0] < 10:
```

Inside `find_lip`: Run the indented block only when this condition is true: `best` is the same object as `None` OR `best[0]` is less than `10`. Other branches handle the remaining case.

### Line 264

```python
        return None
```

Inside `find_lip`: End this function now and send back `None`. A bare return sends None.

### Line 265

```python
    selected_x, selected_y = xs[best[1]], ys[best[1]]
```

Inside `find_lip`: Store the result in `(selected_x, selected_y)`: tuple containing `xs[best[1]]`; `ys[best[1]]`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 266

```python
    if np.ptp(selected_x) < radius * 0.45:
```

Inside `find_lip`: Run the indented block only when this condition is true: `np.ptp`: calculate maximum minus minimum to measure the span. Arguments: `selected_x` is less than (`radius` times `0.45`). Other branches handle the remaining case.

### Line 267

```python
        return None
```

Inside `find_lip`: End this function now and send back `None`. A bare return sends None.

### Line 268

```python
    slope, intercept = np.polyfit(selected_x, selected_y, 1)
```

Inside `find_lip`: Store the result in `(slope, intercept)`: `np.polyfit`: fit polynomial coefficients; degree 1 gives slope and intercept of a straight line. Arguments: `selected_x`; `selected_y`; `1`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 269

```python
    residual = float(np.median(np.abs(selected_y - (slope * selected_x + intercept))))
```

Inside `find_lip`: Store the result in `residual`: `float`: convert a value to a decimal number. Arguments: `np.median`: take the middle value after sorting, reducing the effect of one extreme value. Arguments: `np.abs`: take absolute values element by element. Arguments: (`selected_y` minus ((`slope` times `selected_x`) plus `intercept`)). This is assignment, not an equality check.

### Line 270

```python
    lip_y = float((slope * hip_x + intercept) / ratio)
```

Inside `find_lip`: Store the result in `lip_y`: `float`: convert a value to a decimal number. Arguments: (((`slope` times `hip_x`) plus `intercept`) divided by `ratio`). This is assignment, not an equality check.

### Line 271

```python
    extrapolation = max(selected_x.min() - hip_x, hip_x - selected_x.max(), 0)
```

Inside `find_lip`: Store the result in `extrapolation`: `max`: choose the largest value, or the item with the largest key. Arguments: (`selected_x.min`: find the smallest array value along the specified axis. No arguments are supplied minus `hip_x`); (`hip_x` minus `selected_x.max`: find the largest array value along the specified axis. No arguments are supplied); `0`. This is assignment, not an equality check.

### Line 272

```python
    if extrapolation > radius * 0.65 or not 0 <= lip_y < height:
```

Inside `find_lip`: Run the indented block only when this condition is true: `extrapolation` is greater than (`radius` times `0.65`) OR NOT `0` is at most `lip_y` and is less than `height`. Other branches handle the remaining case.

### Line 273

```python
        return None
```

Inside `find_lip`: End this function now and send back `None`. A bare return sends None.

### Line 274

```python
    confidence = min(1, best[0] / max(12, len(xs)) * (1 - min(0.8, residual / 12)))
```

Inside `find_lip`: Store the result in `confidence`: `min`: choose the smallest value, or the item with the smallest key. Arguments: `1`; ((`best[0]` divided by `max`: choose the largest value, or the item with the largest key. Arguments: `12`; `len`: count items. Arguments: `xs`) times (`1` minus `min`: choose the smallest value, or the item with the smallest key. Arguments: `0.8`; (`residual` divided by `12`))). This is assignment, not an equality check.

### Line 275

```python
    if extrapolation > 0:
```

Inside `find_lip`: Run the indented block only when this condition is true: `extrapolation` is greater than `0`. Other branches handle the remaining case.

### Line 276

```python
        confidence *= 0.65
```

Inside `find_lip`: Update `confidence` using its old value times `0.65`.

### Line 277

```python
    a = [float(selected_x.min() / ratio), float((slope * selected_x.min() + intercept) / ratio)]
```

Inside `find_lip`: Store the result in `a`: list containing `float`: convert a value to a decimal number. Arguments: (`selected_x.min`: find the smallest array value along the specified axis. No arguments are supplied divided by `ratio`); `float`: convert a value to a decimal number. Arguments: (((`slope` times `selected_x.min`: find the smallest array value along the specified axis. No arguments are supplied) plus `intercept`) divided by `ratio`). This is assignment, not an equality check.

### Line 278

```python
    b = [float(selected_x.max() / ratio), float((slope * selected_x.max() + intercept) / ratio)]
```

Inside `find_lip`: Store the result in `b`: list containing `float`: convert a value to a decimal number. Arguments: (`selected_x.max`: find the largest array value along the specified axis. No arguments are supplied divided by `ratio`); `float`: convert a value to a decimal number. Arguments: (((`slope` times `selected_x.max`: find the largest array value along the specified axis. No arguments are supplied) plus `intercept`) divided by `ratio`). This is assignment, not an equality check.

### Line 279

```python
    return dict(a=a, b=b, y=lip_y, score=confidence, extrapolated=bool(extrapolation > 0))
```

Inside `find_lip`: End this function now and send back `dict`: create a dictionary from the named fields. Arguments: a = `a`; b = `b`; y = `lip_y`; score = `confidence`; extrapolated = `bool`: convert a condition to a plain Python True or False. Arguments: `extrapolation` is greater than `0`. A bare return sends None.

### Line 280

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 281

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 282

```python
def annotate(frame, sample):
```

Define `annotate(frame, sample)`. Its job: Draw the evidence for one measurement, with colours matching the app. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 283

```python
    """Draw the evidence for one measurement, with colours matching the app."""
```

Inside `annotate`: Documentation string: Draw the evidence for one measurement, with colours matching the app. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 284

```python
    output = frame.copy()
```

Inside `annotate`: Store the result in `output`: `frame.copy`: make a separate copy so later drawing or changes do not overwrite the original. No arguments are supplied. This is assignment, not an equality check.

### Line 285

```python
    person = sample.get('person')
```

Inside `annotate`: Store the result in `person`: `sample.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'person'`. This is assignment, not an equality check.

### Line 286

```python
    lip = sample.get('lip')
```

Inside `annotate`: Store the result in `lip`: `sample.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'lip'`. This is assignment, not an equality check.

### Line 287

```python
    if person:
```

Inside `annotate`: Run the indented block only when this condition is true: `person`. Other branches handle the remaining case.

### Line 288

```python
        x, y, w, h = map(round, person['box'])
```

Inside `annotate`: Store the result in `(x, y, w, h)`: `map`: apply the first function to each supplied value. Arguments: `round`; `person['box']`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 289

```python
        cv2.rectangle(output, (x, y), (x + w, y + h), (110, 225, 190), 2)
```

Inside `annotate`: Run this operation: `cv2.rectangle`: draw a box or a filled label background on the image. Arguments: `output`; tuple containing `x`; `y`; tuple containing (`x` plus `w`); (`y` plus `h`); tuple containing `110`; `225`; `190`; `2`.

### Line 290

```python
        points = person['points']
```

Inside `annotate`: Store the result in `points`: `person['points']`. This is assignment, not an equality check.

### Line 291

```python
        for a, b in [(5, 6), (5, 11), (6, 12), (11, 12), (11, 13), (12, 14), (13, 15), (14, 16)]:
```

Inside `annotate`: Repeat the following indented block for each `(a, b)` from list containing tuple containing `5`; `6`; tuple containing `5`; `11`; tuple containing `6`; `12`; tuple containing `11`; `12`; tuple containing `11`; `13`; tuple containing `12`; `14`; tuple containing `13`; `15`; tuple containing `14`; `16`. Tuple targets unpack each loop item.

### Line 292

```python
            if min(points[a][2], points[b][2]) > 0.3:
```

Inside `annotate`: Run the indented block only when this condition is true: `min`: choose the smallest value, or the item with the smallest key. Arguments: `points[a][2]`; `points[b][2]` is greater than `0.3`. Other branches handle the remaining case.

### Line 293

```python
                cv2.line(output, tuple(map(round, points[a][:2])), tuple(map(round, points[b][:2])), (110, 225, 190), 2)
```

Inside `annotate`: Run this operation: `cv2.line`: draw a line on the supplied image. Arguments: `output`; `tuple`: create a tuple from the supplied values. Arguments: `map`: apply the first function to each supplied value. Arguments: `round`; `points[a][:2]`; `tuple`: create a tuple from the supplied values. Arguments: `map`: apply the first function to each supplied value. Arguments: `round`; `points[b][:2]`; tuple containing `110`; `225`; `190`; `2`.

### Line 294

```python
        hip = tuple(map(round, person['hip']))
```

Inside `annotate`: Store the result in `hip`: `tuple`: create a tuple from the supplied values. Arguments: `map`: apply the first function to each supplied value. Arguments: `round`; `person['hip']`. This is assignment, not an equality check.

### Line 295

```python
        cv2.circle(output, hip, 6, (80, 225, 255), -1)
```

Inside `annotate`: Run this operation: `cv2.circle`: draw a point marker on the supplied image. Arguments: `output`; `hip`; `6`; tuple containing `80`; `225`; `255`; negative `1`.

### Line 296

```python
        if lip:
```

Inside `annotate`: Run the indented block only when this condition is true: `lip`. Other branches handle the remaining case.

### Line 297

```python
            cv2.line(output, tuple(map(round, lip['a'])), tuple(map(round, lip['b'])), (255, 185, 60), 3)
```

Inside `annotate`: Run this operation: `cv2.line`: draw a line on the supplied image. Arguments: `output`; `tuple`: create a tuple from the supplied values. Arguments: `map`: apply the first function to each supplied value. Arguments: `round`; `lip['a']`; `tuple`: create a tuple from the supplied values. Arguments: `map`: apply the first function to each supplied value. Arguments: `round`; `lip['b']`; tuple containing `255`; `185`; `60`; `3`.

### Line 298

```python
            cv2.line(output, hip, (hip[0], round(lip['y'])), (80, 225, 255), 2)
```

Inside `annotate`: Run this operation: `cv2.line`: draw a line on the supplied image. Arguments: `output`; `hip`; tuple containing `hip[0]`; `round`: round a number to the requested precision. Arguments: `lip['y']`; tuple containing `80`; `225`; `255`; `2`.

### Line 299

```python
    label = sample.get('status', 'Review')
```

Inside `annotate`: Store the result in `label`: `sample.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'status'`; `'Review'`. This is assignment, not an equality check.

### Line 300

```python
    if sample.get('height_px') is not None:
```

Inside `annotate`: Run the indented block only when this condition is true: `sample.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'height_px'` is not the same object as `None`. Other branches handle the remaining case.

### Line 301

```python
        label = f"Hip above local lip: {sample['height_px']:.1f} px | Review required"
```

Inside `annotate`: Store the result in `label`: formatted text `f"Hip above local lip: {sample['height_px']:.1f} px | Review required"`. Inserted values: sample['height_px'], format f'.1f'. This is assignment, not an equality check.

### Line 302

```python
    cv2.rectangle(output, (12, 12), (min(output.shape[1] - 12, 760), 56), (26, 31, 40), -1)
```

Inside `annotate`: Run this operation: `cv2.rectangle`: draw a box or a filled label background on the image. Arguments: `output`; tuple containing `12`; `12`; tuple containing `min`: choose the smallest value, or the item with the smallest key. Arguments: (`output.shape[1]` minus `12`); `760`; `56`; tuple containing `26`; `31`; `40`; negative `1`.

### Line 303

```python
    cv2.putText(output, label, (24, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (240, 240, 240), 2)
```

Inside `annotate`: Run this operation: `cv2.putText`: draw the supplied text on the image. Arguments: `output`; `label`; tuple containing `24`; `42`; `cv2.FONT_HERSHEY_SIMPLEX`; `0.65`; tuple containing `240`; `240`; `240`; `2`.

### Line 304

```python
    return output
```

Inside `annotate`: End this function now and send back `output`. A bare return sends None.

## app.py

Source SHA-256: `82917f9fc8216003d5259e29d7a1947430ba917db246c231a651a8ee4e6bef8a`

### Line 1

```python
"""Lip: automatic video analysis with a native review workspace."""
```

Documentation string: Lip: automatic video analysis with a native review workspace. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 2

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 3

```python
import json
```

Import modules: json. Their functions become available through those module names.

### Line 4

```python
import sys
```

Import modules: sys. Their functions become available through those module names.

### Line 5

```python
from pathlib import Path
```

Import Path from `pathlib`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 6

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 7

```python
import cv2
```

Import modules: cv2. Their functions become available through those module names.

### Line 8

```python
import numpy as np
```

Import modules: numpy under the short name np. Their functions become available through those module names.

### Line 9

```python
from PySide6.QtCore import QThread, Qt, QUrl, Signal
```

Import QThread, Qt, QUrl, Signal from `PySide6.QtCore`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 10

```python
from PySide6.QtGui import QColor, QDesktopServices, QIcon, QImage, QPainter, QPainterPath, QPen, QPixmap
```

Import QColor, QDesktopServices, QIcon, QImage, QPainter, QPainterPath, QPen, QPixmap from `PySide6.QtGui`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 11

```python
from PySide6.QtWidgets import QApplication, QComboBox, QDoubleSpinBox, QFileDialog, QFrame, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QMainWindow, QMessageBox, QProgressBar, QPushButton, QScrollArea, QTabWidget, QTableWidget, QTableWidgetItem, QTextBrowser, QToolButton, QVBoxLayout, QWidget
```

Import QApplication, QComboBox, QDoubleSpinBox, QFileDialog, QFrame, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QMainWindow, QMessageBox, QProgressBar, QPushButton, QScrollArea, QTabWidget, QTableWidget, QTableWidgetItem, QTextBrowser, QToolButton, QVBoxLayout, QWidget from `PySide6.QtWidgets`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 12

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 13

```python
from analysis import analyse, export_csv, open_video, save_report
```

Import analyse, export_csv, open_video, save_report from `analysis`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 14

```python
from measurement import calibrate_height, measure_height
```

Import calibrate_height, measure_height from `measurement`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 15

```python
from vision import annotate, data_folder
```

Import annotate, data_folder from `vision`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 16

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 17

```python
ASSETS = Path(__file__).parent / 'assets'
```

Store the result in `ASSETS`: (`Path(__file__).parent` divided by `'assets'`). This is assignment, not an equality check.

### Line 18

```python
STYLE = '''
```

Store the result in `STYLE`: `"\nQMainWindow, QWidget { background: #ffffff; color: #182334; font-family: 'Segoe UI'; font-size: 12px; }\nQFrame#panel { background: #ffffff; border: 1px solid #e1e7ef; border-radius: 5px; }\nQLabel { background: transparent; }\nQLabel#muted { color: #64748b; }\nQLabel#title { font-size: 24px; font-weight: 600; }\nQLabel#metric { font-size: 27px; font-weight: 600; color: #2563eb; }\nQPushButton { background: #e9eef6; border: 1px solid #dce4ef; padding: 9px 12px; border-radius: 7px; font-weight: 600; }\nQPushButton:hover { background: #dbe7fb; }\nQPushButton:disabled { color: #64748b; background: #f1f5f9; }\nQPushButton#primary { background: #2563eb; color: #ffffff; border: none; }\nQPushButton#primary:hover { background: #1d4ed8; }\nQPushButton#danger { color: #b45343; }\nQLineEdit, QDoubleSpinBox, QComboBox { background: #ffffff; border: 1px solid #dce4ef; border-radius: 6px; padding: 7px; selection-background-color: #bfd5ff; }\nQProgressBar { background: #e9eef6; border: none; border-radius: 4px; height: 7px; }\nQProgressBar::chunk { background: #2563eb; border-radius: 4px; }\nQTableWidget { background: #ffffff; border: 1px solid #e1e7ef; gridline-color: #e9eef6; selection-background-color: #dce9ff; selection-color: #182334; }\nQHeaderView::section { background: #f2f6fc; color: #55657b; padding: 9px; border: none; font-weight: 600; }\nQTabWidget::pane { border: none; }\nQToolButton { border: none; color: #526173; padding: 6px 0; text-align: left; }\nQTabBar::tab { background: #ffffff; color: #64748b; padding: 10px 16px; border-bottom: 2px solid transparent; }\nQTabBar::tab:selected { color: #2563eb; border-bottom-color: #2563eb; }\nQTextBrowser { background: #ffffff; border: none; padding: 18px; }\n"`. This is assignment, not an equality check.

### Line 19

```python
QMainWindow, QWidget { background: #ffffff; color: #182334; font-family: 'Segoe UI'; font-size: 12px; }
```

Qt stylesheet rule for `QMainWindow, QWidget`. Declarations: `background: #ffffff; color: #182334; font-family: 'Segoe UI'; font-size: 12px;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 20

```python
QFrame#panel { background: #ffffff; border: 1px solid #e1e7ef; border-radius: 5px; }
```

Qt stylesheet rule for `QFrame#panel`. Declarations: `background: #ffffff; border: 1px solid #e1e7ef; border-radius: 5px;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 21

```python
QLabel { background: transparent; }
```

Qt stylesheet rule for `QLabel`. Declarations: `background: transparent;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 22

```python
QLabel#muted { color: #64748b; }
```

Qt stylesheet rule for `QLabel#muted`. Declarations: `color: #64748b;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 23

```python
QLabel#title { font-size: 24px; font-weight: 600; }
```

Qt stylesheet rule for `QLabel#title`. Declarations: `font-size: 24px; font-weight: 600;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 24

```python
QLabel#metric { font-size: 27px; font-weight: 600; color: #2563eb; }
```

Qt stylesheet rule for `QLabel#metric`. Declarations: `font-size: 27px; font-weight: 600; color: #2563eb;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 25

```python
QPushButton { background: #e9eef6; border: 1px solid #dce4ef; padding: 9px 12px; border-radius: 7px; font-weight: 600; }
```

Qt stylesheet rule for `QPushButton`. Declarations: `background: #e9eef6; border: 1px solid #dce4ef; padding: 9px 12px; border-radius: 7px; font-weight: 600;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 26

```python
QPushButton:hover { background: #dbe7fb; }
```

Qt stylesheet rule for `QPushButton:hover`. Declarations: `background: #dbe7fb;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 27

```python
QPushButton:disabled { color: #64748b; background: #f1f5f9; }
```

Qt stylesheet rule for `QPushButton:disabled`. Declarations: `color: #64748b; background: #f1f5f9;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 28

```python
QPushButton#primary { background: #2563eb; color: #ffffff; border: none; }
```

Qt stylesheet rule for `QPushButton#primary`. Declarations: `background: #2563eb; color: #ffffff; border: none;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 29

```python
QPushButton#primary:hover { background: #1d4ed8; }
```

Qt stylesheet rule for `QPushButton#primary:hover`. Declarations: `background: #1d4ed8;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 30

```python
QPushButton#danger { color: #b45343; }
```

Qt stylesheet rule for `QPushButton#danger`. Declarations: `color: #b45343;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 31

```python
QLineEdit, QDoubleSpinBox, QComboBox { background: #ffffff; border: 1px solid #dce4ef; border-radius: 6px; padding: 7px; selection-background-color: #bfd5ff; }
```

Qt stylesheet rule for `QLineEdit, QDoubleSpinBox, QComboBox`. Declarations: `background: #ffffff; border: 1px solid #dce4ef; border-radius: 6px; padding: 7px; selection-background-color: #bfd5ff;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 32

```python
QProgressBar { background: #e9eef6; border: none; border-radius: 4px; height: 7px; }
```

Qt stylesheet rule for `QProgressBar`. Declarations: `background: #e9eef6; border: none; border-radius: 4px; height: 7px;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 33

```python
QProgressBar::chunk { background: #2563eb; border-radius: 4px; }
```

Qt stylesheet rule for `QProgressBar::chunk`. Declarations: `background: #2563eb; border-radius: 4px;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 34

```python
QTableWidget { background: #ffffff; border: 1px solid #e1e7ef; gridline-color: #e9eef6; selection-background-color: #dce9ff; selection-color: #182334; }
```

Qt stylesheet rule for `QTableWidget`. Declarations: `background: #ffffff; border: 1px solid #e1e7ef; gridline-color: #e9eef6; selection-background-color: #dce9ff; selection-color: #182334;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 35

```python
QHeaderView::section { background: #f2f6fc; color: #55657b; padding: 9px; border: none; font-weight: 600; }
```

Qt stylesheet rule for `QHeaderView::section`. Declarations: `background: #f2f6fc; color: #55657b; padding: 9px; border: none; font-weight: 600;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 36

```python
QTabWidget::pane { border: none; }
```

Qt stylesheet rule for `QTabWidget::pane`. Declarations: `border: none;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 37

```python
QToolButton { border: none; color: #526173; padding: 6px 0; text-align: left; }
```

Qt stylesheet rule for `QToolButton`. Declarations: `border: none; color: #526173; padding: 6px 0; text-align: left;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 38

```python
QTabBar::tab { background: #ffffff; color: #64748b; padding: 10px 16px; border-bottom: 2px solid transparent; }
```

Qt stylesheet rule for `QTabBar::tab`. Declarations: `background: #ffffff; color: #64748b; padding: 10px 16px; border-bottom: 2px solid transparent;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 39

```python
QTabBar::tab:selected { color: #2563eb; border-bottom-color: #2563eb; }
```

Qt stylesheet rule for `QTabBar::tab:selected`. Declarations: `color: #2563eb; border-bottom-color: #2563eb;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 40

```python
QTextBrowser { background: #ffffff; border: none; padding: 18px; }
```

Qt stylesheet rule for `QTextBrowser`. Declarations: `background: #ffffff; border: none; padding: 18px;`. Background and color use hexadecimal RGB values; padding and sizes use pixels. A #name selects the object name assigned in Python. :hover, :disabled, and :selected select control states. :: selects a control subpart.

### Line 41

```python
'''
```

End the multi-line stylesheet string. The CSS-like text above is data passed to Qt, not Python instructions.

### Line 42

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 43

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 44

```python
def text_label(text, style=None):
```

Define `text_label(text, style=None)`. Its job: Build a wrapping label with an optional named style. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 45

```python
    """Build a wrapping label with an optional named style."""
```

Inside `text_label`: Documentation string: Build a wrapping label with an optional named style. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 46

```python
    label = QLabel(text)
```

Inside `text_label`: Store the result in `label`: `QLabel`: construct the named Qt control or display object. Arguments: `text`. This is assignment, not an equality check.

### Line 47

```python
    label.setWordWrap(True)
```

Inside `text_label`: Run this operation: `label.setWordWrap`: allow long text to wrap across lines. Arguments: `True`.

### Line 48

```python
    if style:
```

Inside `text_label`: Run the indented block only when this condition is true: `style`. Other branches handle the remaining case.

### Line 49

```python
        label.setObjectName(style)
```

Inside `text_label`: Run this operation: `label.setObjectName`: give the control a name used by the stylesheet selector. Arguments: `style`.

### Line 50

```python
    return label
```

Inside `text_label`: End this function now and send back `label`. A bare return sends None.

### Line 51

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 52

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 53

```python
def button(text, action, style=None):
```

Define `button(text, action, style=None)`. Its job: Build a button and connect its click to one action. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 54

```python
    """Build a button and connect its click to one action."""
```

Inside `button`: Documentation string: Build a button and connect its click to one action. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 55

```python
    control = QPushButton(text)
```

Inside `button`: Store the result in `control`: `QPushButton`: construct the named Qt control or display object. Arguments: `text`. This is assignment, not an equality check.

### Line 56

```python
    control.clicked.connect(action)
```

Inside `button`: Run this operation: `control.clicked.connect`: register the function to run when this Qt signal is emitted. Arguments: `action`.

### Line 57

```python
    icon_name = {'browse': 'folder', 'open_session': 'folder', 'start_analysis': 'play', 'stop_analysis': 'stop', 'start_correction': 'edit', 'add_manual': 'plus', 'start_calibration': 'ruler', 'mark_reviewed': 'check', 'exclude': 'close', 'export_results': 'download', 'open_results': 'folder', 'open_review_video': 'play'}.get(action.__name__)
```

Inside `button`: Store the result in `icon_name`: `{'browse': 'folder', 'open_session': 'folder', 'start_analysis': 'play', 'stop_analysis': 'stop', 'start_correction': 'edit', 'add_manual': 'plus', 'start_calibration': 'ruler', 'mark_reviewed': 'check', 'exclude': 'close', 'export_results': 'download', 'open_results': 'folder', 'open_review_video': 'play'}.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `action.__name__`. This is assignment, not an equality check.

### Line 58

```python
    if icon_name:
```

Inside `button`: Run the indented block only when this condition is true: `icon_name`. Other branches handle the remaining case.

### Line 59

```python
        if style == 'primary':
```

Inside `button`: Run the indented block only when this condition is true: `style` equals `'primary'`. Other branches handle the remaining case.

### Line 60

```python
            icon_name += '-white'
```

Inside `button`: Update `icon_name` using its old value plus `'-white'`.

### Line 61

```python
        control.setIcon(QIcon(str(ASSETS / (icon_name + '.svg'))))
```

Inside `button`: Run this operation: `control.setIcon`: call this function with the supplied arguments. Arguments: `QIcon`: construct the named Qt control or display object. Arguments: `str`: convert a value to text. Arguments: (`ASSETS` divided by (`icon_name` plus `'.svg'`)).

### Line 62

```python
    if style:
```

Inside `button`: Run the indented block only when this condition is true: `style`. Other branches handle the remaining case.

### Line 63

```python
        control.setObjectName(style)
```

Inside `button`: Run this operation: `control.setObjectName`: give the control a name used by the stylesheet selector. Arguments: `style`.

### Line 64

```python
    return control
```

Inside `button`: End this function now and send back `control`. A bare return sends None.

### Line 65

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 66

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 67

```python
class VideoCanvas(QLabel):
```

Define the `VideoCanvas` class, inheriting from QLabel. Show a fitted image and convert correction clicks to original pixels.

### Line 68

```python
    """Show a fitted image and convert correction clicks to original pixels."""
```

Inside `VideoCanvas`: Documentation string: Show a fitted image and convert correction clicks to original pixels. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 69

```python

```

Inside `VideoCanvas`: Blank line. It separates related parts for readability and performs no operation.

### Line 70

```python
    point_added = Signal(object)
```

Inside `VideoCanvas`: Store the result in `point_added`: `Signal`: declare a Qt signal that can deliver values to connected functions. Arguments: `object`. This is assignment, not an equality check.

### Line 71

```python

```

Inside `VideoCanvas`: Blank line. It separates related parts for readability and performs no operation.

### Line 72

```python
    def __init__(self):
```

Inside `VideoCanvas`: Define `__init__(self)`. Its job: prepare the new object's state, controls, or runtime resources The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 73

```python
        super().__init__('Choose a video, then click Scan video')
```

Inside `__init__`: Run this operation: `super().__init__`: prepare the new object's state, controls, or runtime resources. Arguments: `'Choose a video, then click Scan video'`.

### Line 74

```python
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
```

Inside `__init__`: Run this operation: `self.setAlignment`: choose where content sits inside this label. Arguments: `Qt.AlignmentFlag.AlignCenter`.

### Line 75

```python
        self.setMinimumSize(400, 240)
```

Inside `__init__`: Run this operation: `self.setMinimumSize`: prevent this widget from becoming smaller than the requested dimensions. Arguments: `400`; `240`.

### Line 76

```python
        self.setStyleSheet('background:#eef2f8; color:#718198; border:1px solid #e9eef6; border-radius:10px;')
```

Inside `__init__`: Run this operation: `self.setStyleSheet`: apply the supplied Qt styling rules. Arguments: `'background:#eef2f8; color:#718198; border:1px solid #e9eef6; border-radius:10px;'`.

### Line 77

```python
        self.frame = None
```

Inside `__init__`: Store the result in `self.frame`: `None`. This is assignment, not an equality check.

### Line 78

```python
        self.correcting = False
```

Inside `__init__`: Store the result in `self.correcting`: `False`. This is assignment, not an equality check.

### Line 79

```python
        self.points = []
```

Inside `__init__`: Store the result in `self.points`: an empty list `[]`. This is assignment, not an equality check.

### Line 80

```python
        self.click_limit = 3
```

Inside `__init__`: Store the result in `self.click_limit`: `3`. This is assignment, not an equality check.

### Line 81

```python

```

Inside `VideoCanvas`: Blank line. It separates related parts for readability and performs no operation.

### Line 82

```python
    def show_frame(self, frame):
```

Inside `VideoCanvas`: Define `show_frame(self, frame)`. Its job: copy a video frame, convert its colours, and fit it inside the canvas The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 83

```python
        self.frame = frame.copy()
```

Inside `show_frame`: Store the result in `self.frame`: `frame.copy`: make a separate copy so later drawing or changes do not overwrite the original. No arguments are supplied. This is assignment, not an equality check.

### Line 84

```python
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
```

Inside `show_frame`: Store the result in `rgb`: `cv2.cvtColor`: convert between colour representations. Arguments: `frame`; `cv2.COLOR_BGR2RGB`. This is assignment, not an equality check.

### Line 85

```python
        image = QImage(rgb.data, rgb.shape[1], rgb.shape[0], rgb.strides[0], QImage.Format.Format_RGB888).copy()
```

Inside `show_frame`: Store the result in `image`: `QImage(rgb.data, rgb.shape[1], rgb.shape[0], rgb.strides[0], QImage.Format.Format_RGB888).copy`: make a separate copy so later drawing or changes do not overwrite the original. No arguments are supplied. This is assignment, not an equality check.

### Line 86

```python
        self.original = QPixmap.fromImage(image)
```

Inside `show_frame`: Store the result in `self.original`: `QPixmap.fromImage`: convert a Qt image to a displayable pixmap. Arguments: `image`. This is assignment, not an equality check.

### Line 87

```python
        self.setPixmap(self.original.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
```

Inside `show_frame`: Run this operation: `self.setPixmap`: show a pixmap in the image label. Arguments: `self.original.scaled`: produce a resized pixmap while respecting the selected aspect-ratio and smoothing options. Arguments: `self.size`: call this function with the supplied arguments. No arguments are supplied; `Qt.AspectRatioMode.KeepAspectRatio`; `Qt.TransformationMode.SmoothTransformation`.

### Line 88

```python

```

Inside `VideoCanvas`: Blank line. It separates related parts for readability and performs no operation.

### Line 89

```python
    def resizeEvent(self, event):
```

Inside `VideoCanvas`: Define `resizeEvent(self, event)`. Its job: redraw the fitted image after the widget changes size The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 90

```python
        super().resizeEvent(event)
```

Inside `resizeEvent`: Run this operation: `super().resizeEvent`: redraw the fitted image after the widget changes size. Arguments: `event`.

### Line 91

```python
        if self.frame is not None:
```

Inside `resizeEvent`: Run the indented block only when this condition is true: `self.frame` is not the same object as `None`. Other branches handle the remaining case.

### Line 92

```python
            self.show_frame(self.frame)
```

Inside `resizeEvent`: Run this operation: `self.show_frame`: copy a video frame, convert its colours, and fit it inside the canvas. Arguments: `self.frame`.

### Line 93

```python

```

Inside `VideoCanvas`: Blank line. It separates related parts for readability and performs no operation.

### Line 94

```python
    def mousePressEvent(self, event):
```

Inside `VideoCanvas`: Define `mousePressEvent(self, event)`. Its job: handle a mouse click in this widget The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 95

```python
        if not self.correcting or self.frame is None or len(self.points) >= self.click_limit:
```

Inside `mousePressEvent`: Run the indented block only when this condition is true: NOT `self.correcting` OR `self.frame` is the same object as `None` OR `len`: count items. Arguments: `self.points` is at least `self.click_limit`. Other branches handle the remaining case.

### Line 96

```python
            return
```

Inside `mousePressEvent`: End this function now and send back no explicit value. A bare return sends None.

### Line 97

```python
        ratio = min(self.width() / self.frame.shape[1], self.height() / self.frame.shape[0])
```

Inside `mousePressEvent`: Store the result in `ratio`: `min`: choose the smallest value, or the item with the smallest key. Arguments: (`self.width`: read this widget's current width. No arguments are supplied divided by `self.frame.shape[1]`); (`self.height`: read this widget's current height. No arguments are supplied divided by `self.frame.shape[0]`). This is assignment, not an equality check.

### Line 98

```python
        offset_x = (self.width() - self.frame.shape[1] * ratio) / 2
```

Inside `mousePressEvent`: Store the result in `offset_x`: ((`self.width`: read this widget's current width. No arguments are supplied minus (`self.frame.shape[1]` times `ratio`)) divided by `2`). This is assignment, not an equality check.

### Line 99

```python
        offset_y = (self.height() - self.frame.shape[0] * ratio) / 2
```

Inside `mousePressEvent`: Store the result in `offset_y`: ((`self.height`: read this widget's current height. No arguments are supplied minus (`self.frame.shape[0]` times `ratio`)) divided by `2`). This is assignment, not an equality check.

### Line 100

```python
        x, y = (event.position().x() - offset_x) / ratio, (event.position().y() - offset_y) / ratio
```

Inside `mousePressEvent`: Store the result in `(x, y)`: tuple containing ((`event.position().x`: read the horizontal coordinate. No arguments are supplied minus `offset_x`) divided by `ratio`); ((`event.position().y`: read the vertical coordinate. No arguments are supplied minus `offset_y`) divided by `ratio`). Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 101

```python
        if 0 <= x < self.frame.shape[1] and 0 <= y < self.frame.shape[0]:
```

Inside `mousePressEvent`: Run the indented block only when this condition is true: `0` is at most `x` and is less than `self.frame.shape[1]` AND `0` is at most `y` and is less than `self.frame.shape[0]`. Other branches handle the remaining case.

### Line 102

```python
            self.points.append((x, y))
```

Inside `mousePressEvent`: Run this operation: `self.points.append`: add an item to the end of this list. Arguments: tuple containing `x`; `y`.

### Line 103

```python
            self.point_added.emit(self.points.copy())
```

Inside `mousePressEvent`: Run this operation: `self.point_added.emit`: send this Qt signal to its connected receivers. Arguments: `self.points.copy`: make a separate copy so later drawing or changes do not overwrite the original. No arguments are supplied.

### Line 104

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 105

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 106

```python
class HeightChart(QWidget):
```

Define the `HeightChart` class, inheriting from QWidget. Draw sampled gaps and let a click select the nearest candidate.

### Line 107

```python
    """Draw sampled gaps and let a click select the nearest candidate."""
```

Inside `HeightChart`: Documentation string: Draw sampled gaps and let a click select the nearest candidate. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 108

```python

```

Inside `HeightChart`: Blank line. It separates related parts for readability and performs no operation.

### Line 109

```python
    selected = Signal(int)
```

Inside `HeightChart`: Store the result in `selected`: `Signal`: declare a Qt signal that can deliver values to connected functions. Arguments: `int`. This is assignment, not an equality check.

### Line 110

```python

```

Inside `HeightChart`: Blank line. It separates related parts for readability and performs no operation.

### Line 111

```python
    def __init__(self):
```

Inside `HeightChart`: Define `__init__(self)`. Its job: prepare the new object's state, controls, or runtime resources The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 112

```python
        super().__init__()
```

Inside `__init__`: Run this operation: `super().__init__`: prepare the new object's state, controls, or runtime resources. No arguments are supplied.

### Line 113

```python
        self.report = None
```

Inside `__init__`: Store the result in `self.report`: `None`. This is assignment, not an equality check.

### Line 114

```python
        self.setMinimumHeight(110)
```

Inside `__init__`: Run this operation: `self.setMinimumHeight`: reserve enough vertical room for this widget. Arguments: `110`.

### Line 115

```python

```

Inside `HeightChart`: Blank line. It separates related parts for readability and performs no operation.

### Line 116

```python
    def paintEvent(self, event):
```

Inside `HeightChart`: Define `paintEvent(self, event)`. Its job: draw the timeline into this widget using Qt's painting API The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 117

```python
        painter = QPainter(self)
```

Inside `paintEvent`: Store the result in `painter`: `QPainter`: create the object that draws inside a Qt widget. Arguments: `self`. This is assignment, not an equality check.

### Line 118

```python
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
```

Inside `paintEvent`: Run this operation: `painter.setRenderHint`: enable smooth drawing of lines and shapes. Arguments: `QPainter.RenderHint.Antialiasing`.

### Line 119

```python
        painter.fillRect(self.rect(), QColor('#ffffff'))
```

Inside `paintEvent`: Run this operation: `painter.fillRect`: paint a rectangular background. Arguments: `self.rect`: get the widget's full local rectangle. No arguments are supplied; `QColor`: create a drawing colour from a name or hexadecimal code. Arguments: `'#ffffff'`.

### Line 120

```python
        painter.setPen(QColor('#718198'))
```

Inside `paintEvent`: Run this operation: `painter.setPen`: select the colour and width of future drawn outlines. Arguments: `QColor`: create a drawing colour from a name or hexadecimal code. Arguments: `'#718198'`.

### Line 121

```python
        painter.drawText(16, 20, 'HIP ABOVE LIP  /  IMAGE PIXELS')
```

Inside `paintEvent`: Run this operation: `painter.drawText`: paint text at the supplied location. Arguments: `16`; `20`; `'HIP ABOVE LIP  /  IMAGE PIXELS'`.

### Line 122

```python
        if not self.report or not self.report['samples']:
```

Inside `paintEvent`: Run the indented block only when this condition is true: NOT `self.report` OR NOT `self.report['samples']`. Other branches handle the remaining case.

### Line 123

```python
            painter.drawText(16, 60, 'The measurement timeline appears after analysis.')
```

Inside `paintEvent`: Run this operation: `painter.drawText`: paint text at the supplied location. Arguments: `16`; `60`; `'The measurement timeline appears after analysis.'`.

### Line 124

```python
            return
```

Inside `paintEvent`: End this function now and send back no explicit value. A bare return sends None.

### Line 125

```python
        heights = [item['height_px'] for item in self.report['samples'] if item['height_px'] is not None]
```

Inside `paintEvent`: Store the result in `heights`: produce `item['height_px']`, for each item in `self.report['samples']`, keeping only `item['height_px']` is not the same object as `None`. This is assignment, not an equality check.

### Line 126

```python
        limit = max(50, float(np.percentile(np.abs(heights), 90))) if heights else 50
```

Inside `paintEvent`: Store the result in `limit`: `max`: choose the largest value, or the item with the largest key. Arguments: `50`; `float`: convert a value to a decimal number. Arguments: `np.percentile`: find a percentile for a robust chart display scale. Arguments: `np.abs`: take absolute values element by element. Arguments: `heights`; `90` when `heights`; otherwise `50`. This is assignment, not an equality check.

### Line 127

```python
        begin, span = self.report['start'], max(0.01, self.report['end'] - self.report['start'])
```

Inside `paintEvent`: Store the result in `(begin, span)`: tuple containing `self.report['start']`; `max`: choose the largest value, or the item with the largest key. Arguments: `0.01`; (`self.report['end']` minus `self.report['start']`). Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 128

```python
        baseline = self.height() * 0.62
```

Inside `paintEvent`: Store the result in `baseline`: (`self.height`: read this widget's current height. No arguments are supplied times `0.62`). This is assignment, not an equality check.

### Line 129

```python
        painter.setPen(QPen(QColor('#d5ddea'), 1))
```

Inside `paintEvent`: Run this operation: `painter.setPen`: select the colour and width of future drawn outlines. Arguments: `QPen`: set a line's colour and width. Arguments: `QColor`: create a drawing colour from a name or hexadecimal code. Arguments: `'#d5ddea'`; `1`.

### Line 130

```python
        painter.drawLine(16, round(baseline), self.width() - 16, round(baseline))
```

Inside `paintEvent`: Run this operation: `painter.drawLine`: paint a straight line between the supplied endpoints. Arguments: `16`; `round`: round a number to the requested precision. Arguments: `baseline`; (`self.width`: read this widget's current width. No arguments are supplied minus `16`); `round`: round a number to the requested precision. Arguments: `baseline`.

### Line 131

```python
        path, connected = QPainterPath(), False
```

Inside `paintEvent`: Store the result in `(path, connected)`: tuple containing `QPainterPath`: create a path that can contain disconnected timeline segments. No arguments are supplied; `False`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 132

```python
        samples = sorted(self.report['samples'], key=lambda item: item['time'])
```

Inside `paintEvent`: Store the result in `samples`: `sorted`: produce an ordered copy of the supplied items. Arguments: `self.report['samples']`; key = a short function taking `item` and returning `item['time']`. This is assignment, not an equality check.

### Line 133

```python
        for sample in samples[::max(1, len(samples) // 1500)]:
```

Inside `paintEvent`: Repeat the following indented block for each `sample` from `samples[::max(1, len(samples) // 1500)]`. Tuple targets unpack each loop item.

### Line 134

```python
            if sample['height_px'] is None or sample.get('cut'):
```

Inside `paintEvent`: Run the indented block only when this condition is true: `sample['height_px']` is the same object as `None` OR `sample.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'cut'`. Other branches handle the remaining case.

### Line 135

```python
                connected = False
```

Inside `paintEvent`: Store the result in `connected`: `False`. This is assignment, not an equality check.

### Line 136

```python
                continue
```

Inside `paintEvent`: Skip the rest of this loop iteration and try the next item. This rejects the current unsuitable detection, fit, or sample.

### Line 137

```python
            x = 16 + (sample['time'] - begin) / span * (self.width() - 32)
```

Inside `paintEvent`: Store the result in `x`: (`16` plus (((`sample['time']` minus `begin`) divided by `span`) times (`self.width`: read this widget's current width. No arguments are supplied minus `32`))). This is assignment, not an equality check.

### Line 138

```python
            y = baseline - np.clip(sample['height_px'] / limit, -1, 1) * (self.height() * 0.32)
```

Inside `paintEvent`: Store the result in `y`: (`baseline` minus (`np.clip`: limit values to the supplied lower and upper bounds. Arguments: (`sample['height_px']` divided by `limit`); negative `1`; `1` times (`self.height`: read this widget's current height. No arguments are supplied times `0.32`))). This is assignment, not an equality check.

### Line 139

```python
            if connected:
```

Inside `paintEvent`: Run the indented block only when this condition is true: `connected`. Other branches handle the remaining case.

### Line 140

```python
                path.lineTo(float(x), float(y))
```

Inside `paintEvent`: Run this operation: `path.lineTo`: extend the existing path to this position. Arguments: `float`: convert a value to a decimal number. Arguments: `x`; `float`: convert a value to a decimal number. Arguments: `y`.

### Line 141

```python
            else:
```

Inside `paintEvent`: Run this branch when the preceding condition was false.

### Line 142

```python
                path.moveTo(float(x), float(y))
```

Inside `paintEvent`: Run this operation: `path.moveTo`: start a new disconnected path segment at this position. Arguments: `float`: convert a value to a decimal number. Arguments: `x`; `float`: convert a value to a decimal number. Arguments: `y`.

### Line 143

```python
            connected = True
```

Inside `paintEvent`: Store the result in `connected`: `True`. This is assignment, not an equality check.

### Line 144

```python
        painter.setPen(QPen(QColor('#2563eb'), 1.5))
```

Inside `paintEvent`: Run this operation: `painter.setPen`: select the colour and width of future drawn outlines. Arguments: `QPen`: set a line's colour and width. Arguments: `QColor`: create a drawing colour from a name or hexadecimal code. Arguments: `'#2563eb'`; `1.5`.

### Line 145

```python
        painter.drawPath(path)
```

Inside `paintEvent`: Run this operation: `painter.drawPath`: paint the accumulated timeline path. Arguments: `path`.

### Line 146

```python
        for jump in self.report['jumps']:
```

Inside `paintEvent`: Repeat the following indented block for each `jump` from `self.report['jumps']`. Tuple targets unpack each loop item.

### Line 147

```python
            x = 16 + (jump['peak_time'] - begin) / span * (self.width() - 32)
```

Inside `paintEvent`: Store the result in `x`: (`16` plus (((`jump['peak_time']` minus `begin`) divided by `span`) times (`self.width`: read this widget's current width. No arguments are supplied minus `32`))). This is assignment, not an equality check.

### Line 148

```python
            painter.setBrush(QColor('#2563eb') if not jump['excluded'] else QColor('#a2acba'))
```

Inside `paintEvent`: Run this operation: `painter.setBrush`: select the fill colour of future shapes. Arguments: `QColor`: create a drawing colour from a name or hexadecimal code. Arguments: `'#2563eb'` when NOT `jump['excluded']`; otherwise `QColor`: create a drawing colour from a name or hexadecimal code. Arguments: `'#a2acba'`.

### Line 149

```python
            painter.drawEllipse(round(x) - 3, round(baseline) - 3, 6, 6)
```

Inside `paintEvent`: Run this operation: `painter.drawEllipse`: paint a circular candidate marker. Arguments: (`round`: round a number to the requested precision. Arguments: `x` minus `3`); (`round`: round a number to the requested precision. Arguments: `baseline` minus `3`); `6`; `6`.

### Line 150

```python
        painter.setPen(QColor('#718198'))
```

Inside `paintEvent`: Run this operation: `painter.setPen`: select the colour and width of future drawn outlines. Arguments: `QColor`: create a drawing colour from a name or hexadecimal code. Arguments: `'#718198'`.

### Line 151

```python
        painter.drawText(16, self.height() - 7, f'{begin:.1f}s')
```

Inside `paintEvent`: Run this operation: `painter.drawText`: paint text at the supplied location. Arguments: `16`; (`self.height`: read this widget's current height. No arguments are supplied minus `7`); formatted text `f'{begin:.1f}s'`. Inserted values: begin, format f'.1f'.

### Line 152

```python
        painter.drawText(self.width() - 80, self.height() - 7, f"{self.report['end']:.1f}s")
```

Inside `paintEvent`: Run this operation: `painter.drawText`: paint text at the supplied location. Arguments: (`self.width`: read this widget's current width. No arguments are supplied minus `80`); (`self.height`: read this widget's current height. No arguments are supplied minus `7`); formatted text `f"{self.report['end']:.1f}s"`. Inserted values: self.report['end'], format f'.1f'.

### Line 153

```python

```

Inside `HeightChart`: Blank line. It separates related parts for readability and performs no operation.

### Line 154

```python
    def mousePressEvent(self, event):
```

Inside `HeightChart`: Define `mousePressEvent(self, event)`. Its job: handle a mouse click in this widget The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 155

```python
        if self.report and self.report['jumps']:
```

Inside `mousePressEvent`: Run the indented block only when this condition is true: `self.report` AND `self.report['jumps']`. Other branches handle the remaining case.

### Line 156

```python
            time = self.report['start'] + (event.position().x() - 16) / max(1, self.width() - 32) * (self.report['end'] - self.report['start'])
```

Inside `mousePressEvent`: Store the result in `time`: (`self.report['start']` plus (((`event.position().x`: read the horizontal coordinate. No arguments are supplied minus `16`) divided by `max`: choose the largest value, or the item with the largest key. Arguments: `1`; (`self.width`: read this widget's current width. No arguments are supplied minus `32`)) times (`self.report['end']` minus `self.report['start']`))). This is assignment, not an equality check.

### Line 157

```python
            index = min(range(len(self.report['jumps'])), key=lambda i: abs(self.report['jumps'][i]['peak_time'] - time))
```

Inside `mousePressEvent`: Store the result in `index`: `min`: choose the smallest value, or the item with the smallest key. Arguments: `range`: produce integer loop positions, excluding the upper bound. Arguments: `len`: count items. Arguments: `self.report['jumps']`; key = a short function taking `i` and returning `abs`: call this function with the supplied arguments. Arguments: (`self.report['jumps'][i]['peak_time']` minus `time`). This is assignment, not an equality check.

### Line 158

```python
            self.selected.emit(index)
```

Inside `mousePressEvent`: Run this operation: `self.selected.emit`: send this Qt signal to its connected receivers. Arguments: `index`.

### Line 159

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 160

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 161

```python
class AnalysisWorker(QThread):
```

Define the `AnalysisWorker` class, inheriting from QThread. Keep video decoding and model inference off the window thread.

### Line 162

```python
    """Keep video decoding and model inference off the window thread."""
```

Inside `AnalysisWorker`: Documentation string: Keep video decoding and model inference off the window thread. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 163

```python

```

Inside `AnalysisWorker`: Blank line. It separates related parts for readability and performs no operation.

### Line 164

```python
    progress = Signal(object)
```

Inside `AnalysisWorker`: Store the result in `progress`: `Signal`: declare a Qt signal that can deliver values to connected functions. Arguments: `object`. This is assignment, not an equality check.

### Line 165

```python
    preview = Signal(object)
```

Inside `AnalysisWorker`: Store the result in `preview`: `Signal`: declare a Qt signal that can deliver values to connected functions. Arguments: `object`. This is assignment, not an equality check.

### Line 166

```python
    result = Signal(object)
```

Inside `AnalysisWorker`: Store the result in `result`: `Signal`: declare a Qt signal that can deliver values to connected functions. Arguments: `object`. This is assignment, not an equality check.

### Line 167

```python
    failed = Signal(str)
```

Inside `AnalysisWorker`: Store the result in `failed`: `Signal`: declare a Qt signal that can deliver values to connected functions. Arguments: `str`. This is assignment, not an equality check.

### Line 168

```python

```

Inside `AnalysisWorker`: Blank line. It separates related parts for readability and performs no operation.

### Line 169

```python
    def __init__(self, settings):
```

Inside `AnalysisWorker`: Define `__init__(self, settings)`. Its job: prepare the new object's state, controls, or runtime resources The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 170

```python
        super().__init__()
```

Inside `__init__`: Run this operation: `super().__init__`: prepare the new object's state, controls, or runtime resources. No arguments are supplied.

### Line 171

```python
        self.settings = settings
```

Inside `__init__`: Store the result in `self.settings`: `settings`. This is assignment, not an equality check.

### Line 172

```python

```

Inside `AnalysisWorker`: Blank line. It separates related parts for readability and performs no operation.

### Line 173

```python
    def run(self):
```

Inside `AnalysisWorker`: Define `run(self)`. Its job: perform this worker's background task and emit its outcome The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 174

```python
        try:
```

Inside `run`: Begin an operation with explicit error handling. The following except clauses handle failures; finally performs cleanup even after a return or error.

### Line 175

```python
            report = analyse(**self.settings, progress=self.progress.emit, preview=self.preview.emit, cancelled=self.isInterruptionRequested)
```

Inside `run`: Store the result in `report`: `analyse`: process the selected video range, store evidence, group candidates, and save outputs. Arguments: ** = `self.settings`; progress = `self.progress.emit`; preview = `self.preview.emit`; cancelled = `self.isInterruptionRequested`. This is assignment, not an equality check.

### Line 176

```python
            self.result.emit(report)
```

Inside `run`: Run this operation: `self.result.emit`: send this Qt signal to its connected receivers. Arguments: `report`.

### Line 177

```python
        except InterruptedError:
```

Inside `run`: Handle the exception type(s) named here. `as error` stores the exception so a readable message can be shown or saved.

### Line 178

```python
            self.failed.emit('Stopped before analysis started. Existing sessions are safe.')
```

Inside `run`: Run this operation: `self.failed.emit`: send this Qt signal to its connected receivers. Arguments: `'Stopped before analysis started. Existing sessions are safe.'`.

### Line 179

```python
        except Exception as error:
```

Inside `run`: Handle the exception type(s) named here. `as error` stores the exception so a readable message can be shown or saved.

### Line 180

```python
            self.failed.emit(str(error))
```

Inside `run`: Run this operation: `self.failed.emit`: send this Qt signal to its connected receivers. Arguments: `str`: convert a value to text. Arguments: `error`.

### Line 181

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 182

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 183

```python
class FrameWorker(QThread):
```

Define the `FrameWorker` class, inheriting from QThread. Read the original selected frame without blocking the window.

### Line 184

```python
    """Read the original selected frame without blocking the window."""
```

Inside `FrameWorker`: Documentation string: Read the original selected frame without blocking the window. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 185

```python

```

Inside `FrameWorker`: Blank line. It separates related parts for readability and performs no operation.

### Line 186

```python
    loaded = Signal(object)
```

Inside `FrameWorker`: Store the result in `loaded`: `Signal`: declare a Qt signal that can deliver values to connected functions. Arguments: `object`. This is assignment, not an equality check.

### Line 187

```python
    failed = Signal(str)
```

Inside `FrameWorker`: Store the result in `failed`: `Signal`: declare a Qt signal that can deliver values to connected functions. Arguments: `str`. This is assignment, not an equality check.

### Line 188

```python

```

Inside `FrameWorker`: Blank line. It separates related parts for readability and performs no operation.

### Line 189

```python
    def __init__(self, source, frame):
```

Inside `FrameWorker`: Define `__init__(self, source, frame)`. Its job: prepare the new object's state, controls, or runtime resources The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 190

```python
        super().__init__()
```

Inside `__init__`: Run this operation: `super().__init__`: prepare the new object's state, controls, or runtime resources. No arguments are supplied.

### Line 191

```python
        self.source, self.frame = source, frame
```

Inside `__init__`: Store the result in `(self.source, self.frame)`: tuple containing `source`; `frame`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 192

```python

```

Inside `FrameWorker`: Blank line. It separates related parts for readability and performs no operation.

### Line 193

```python
    def run(self):
```

Inside `FrameWorker`: Define `run(self)`. Its job: perform this worker's background task and emit its outcome The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 194

```python
        capture = None
```

Inside `run`: Store the result in `capture`: `None`. This is assignment, not an equality check.

### Line 195

```python
        try:
```

Inside `run`: Begin an operation with explicit error handling. The following except clauses handle failures; finally performs cleanup even after a return or error.

### Line 196

```python
            capture, fps, count = open_video(self.source)
```

Inside `run`: Store the result in `(capture, fps, count)`: `open_video`: open a source through FFmpeg and validate its video metadata. Arguments: `self.source`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 197

```python
            capture.set(cv2.CAP_PROP_POS_FRAMES, self.frame)
```

Inside `run`: Run this operation: `capture.set`: set a video reader property, such as its next frame position. Arguments: `cv2.CAP_PROP_POS_FRAMES`; `self.frame`.

### Line 198

```python
            ok, image = capture.read()
```

Inside `run`: Store the result in `(ok, image)`: `capture.read`: read the next frame or next byte chunk from this resource. No arguments are supplied. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 199

```python
            if not ok:
```

Inside `run`: Run the indented block only when this condition is true: NOT `ok`. Other branches handle the remaining case.

### Line 200

```python
                raise ValueError('Could not load the original frame. Check that the video is still available.')
```

Inside `run`: Stop this operation by raising an exception: `ValueError`: call this function with the supplied arguments. Arguments: `'Could not load the original frame. Check that the video is still available.'`. A matching except block can handle it.

### Line 201

```python
            self.loaded.emit(image)
```

Inside `run`: Run this operation: `self.loaded.emit`: send this Qt signal to its connected receivers. Arguments: `image`.

### Line 202

```python
        except Exception as error:
```

Inside `run`: Handle the exception type(s) named here. `as error` stores the exception so a readable message can be shown or saved.

### Line 203

```python
            self.failed.emit(str(error))
```

Inside `run`: Run this operation: `self.failed.emit`: send this Qt signal to its connected receivers. Arguments: `str`: convert a value to text. Arguments: `error`.

### Line 204

```python
        finally:
```

Inside `run`: Always run the following cleanup block, whether processing succeeds, returns early, or raises an error.

### Line 205

```python
            if capture is not None:
```

Inside `run`: Run the indented block only when this condition is true: `capture` is not the same object as `None`. Other branches handle the remaining case.

### Line 206

```python
                capture.release()
```

Inside `run`: Run this operation: `capture.release`: close the video reader or finalize the video writer. No arguments are supplied.

### Line 207

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 208

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 209

```python
class MainWindow(QMainWindow):
```

Define the `MainWindow` class, inheriting from QMainWindow. Own the controls, review canvas, result table, and session state.

### Line 210

```python
    """Own the controls, review canvas, result table, and session state."""
```

Inside `MainWindow`: Documentation string: Own the controls, review canvas, result table, and session state. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 211

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 212

```python
    def __init__(self):
```

Inside `MainWindow`: Define `__init__(self)`. Its job: prepare the new object's state, controls, or runtime resources The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 213

```python
        super().__init__()
```

Inside `__init__`: Run this operation: `super().__init__`: prepare the new object's state, controls, or runtime resources. No arguments are supplied.

### Line 214

```python
        self.report = self.worker = self.frame_worker = None
```

Inside `__init__`: Store the result in `self.report`, `self.worker`, `self.frame_worker`: `None`. This is assignment, not an equality check.

### Line 215

```python
        self.close_pending = False
```

Inside `__init__`: Store the result in `self.close_pending`: `False`. This is assignment, not an equality check.

### Line 216

```python
        self.raw_frame = None
```

Inside `__init__`: Store the result in `self.raw_frame`: `None`. This is assignment, not an equality check.

### Line 217

```python
        self.pending_manual = None
```

Inside `__init__`: Store the result in `self.pending_manual`: `None`. This is assignment, not an equality check.

### Line 218

```python
        self.correction_mode = 'points'
```

Inside `__init__`: Store the result in `self.correction_mode`: `'points'`. This is assignment, not an equality check.

### Line 219

```python
        self.setWindowTitle('Lip | Prototype-2')
```

Inside `__init__`: Run this operation: `self.setWindowTitle`: set the text in the window title bar. Arguments: `'Lip | Prototype-2'`.

### Line 220

```python
        self.setWindowIcon(QIcon(str(ASSETS / 'icon.ico')))
```

Inside `__init__`: Run this operation: `self.setWindowIcon`: set the title-bar and taskbar icon. Arguments: `QIcon`: construct the named Qt control or display object. Arguments: `str`: convert a value to text. Arguments: (`ASSETS` divided by `'icon.ico'`).

### Line 221

```python
        self.resize(1220, 860)
```

Inside `__init__`: Run this operation: `self.resize`: request an initial window size. Arguments: `1220`; `860`.

### Line 222

```python
        self.setMinimumSize(1020, 720)
```

Inside `__init__`: Run this operation: `self.setMinimumSize`: prevent this widget from becoming smaller than the requested dimensions. Arguments: `1020`; `720`.

### Line 223

```python
        self.setAcceptDrops(True)
```

Inside `__init__`: Run this operation: `self.setAcceptDrops`: allow dragged files or links to enter this window. Arguments: `True`.

### Line 224

```python
        container = QWidget()
```

Inside `__init__`: Store the result in `container`: `QWidget`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 225

```python
        self.setCentralWidget(container)
```

Inside `__init__`: Run this operation: `self.setCentralWidget`: install the main content widget in the window. Arguments: `container`.

### Line 226

```python
        layout = QVBoxLayout(container)
```

Inside `__init__`: Store the result in `layout`: `QVBoxLayout`: construct the named Qt control or display object. Arguments: `container`. This is assignment, not an equality check.

### Line 227

```python
        layout.setContentsMargins(24, 18, 24, 18)
```

Inside `__init__`: Run this operation: `layout.setContentsMargins`: set inner spacing at the left, top, right, and bottom. Arguments: `24`; `18`; `24`; `18`.

### Line 228

```python
        header = QHBoxLayout()
```

Inside `__init__`: Store the result in `header`: `QHBoxLayout`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 229

```python
        logo = QLabel()
```

Inside `__init__`: Store the result in `logo`: `QLabel`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 230

```python
        logo.setPixmap(QIcon(str(ASSETS / 'icon.svg')).pixmap(38, 38))
```

Inside `__init__`: Run this operation: `logo.setPixmap`: show a pixmap in the image label. Arguments: `QIcon(str(ASSETS / 'icon.svg')).pixmap`: call this function with the supplied arguments. Arguments: `38`; `38`.

### Line 231

```python
        header.addWidget(logo)
```

Inside `__init__`: Run this operation: `header.addWidget`: put a control into this layout. Arguments: `logo`.

### Line 232

```python
        header.addWidget(text_label('Lip', 'title'))
```

Inside `__init__`: Run this operation: `header.addWidget`: put a control into this layout. Arguments: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'Lip'`; `'title'`.

### Line 233

```python
        header.addStretch()
```

Inside `__init__`: Run this operation: `header.addStretch`: add flexible empty space that pushes neighbouring controls apart. No arguments are supplied.

### Line 234

```python
        header.addWidget(text_label('HALFPIPE REVIEW  /  PROTOTYPE 2', 'muted'))
```

Inside `__init__`: Run this operation: `header.addWidget`: put a control into this layout. Arguments: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'HALFPIPE REVIEW  /  PROTOTYPE 2'`; `'muted'`.

### Line 235

```python
        layout.addLayout(header)
```

Inside `__init__`: Run this operation: `layout.addLayout`: put another layout into this layout. Arguments: `header`.

### Line 236

```python
        self.tabs = QTabWidget()
```

Inside `__init__`: Store the result in `self.tabs`: `QTabWidget`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 237

```python
        layout.addWidget(self.tabs)
```

Inside `__init__`: Run this operation: `layout.addWidget`: put a control into this layout. Arguments: `self.tabs`.

### Line 238

```python
        workspace = QWidget()
```

Inside `__init__`: Store the result in `workspace`: `QWidget`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 239

```python
        self.tabs.addTab(workspace, 'Analyse & review')
```

Inside `__init__`: Run this operation: `self.tabs.addTab`: add a labelled page to the tab control. Arguments: `workspace`; `'Analyse & review'`.

### Line 240

```python
        body = QHBoxLayout(workspace)
```

Inside `__init__`: Store the result in `body`: `QHBoxLayout`: construct the named Qt control or display object. Arguments: `workspace`. This is assignment, not an equality check.

### Line 241

```python
        body.setContentsMargins(0, 12, 0, 0)
```

Inside `__init__`: Run this operation: `body.setContentsMargins`: set inner spacing at the left, top, right, and bottom. Arguments: `0`; `12`; `0`; `0`.

### Line 242

```python
        left = QVBoxLayout()
```

Inside `__init__`: Store the result in `left`: `QVBoxLayout`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 243

```python
        body.addLayout(left, 3)
```

Inside `__init__`: Run this operation: `body.addLayout`: put another layout into this layout. Arguments: `left`; `3`.

### Line 244

```python
        summary = QHBoxLayout()
```

Inside `__init__`: Store the result in `summary`: `QHBoxLayout`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 245

```python
        summary.addWidget(text_label('Jumps: ', 'muted'))
```

Inside `__init__`: Run this operation: `summary.addWidget`: put a control into this layout. Arguments: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'Jumps: '`; `'muted'`.

### Line 246

```python
        self.candidate_metric = text_label('0')
```

Inside `__init__`: Store the result in `self.candidate_metric`: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'0'`. This is assignment, not an equality check.

### Line 247

```python
        summary.addWidget(self.candidate_metric)
```

Inside `__init__`: Run this operation: `summary.addWidget`: put a control into this layout. Arguments: `self.candidate_metric`.

### Line 248

```python
        summary.addStretch()
```

Inside `__init__`: Run this operation: `summary.addStretch`: add flexible empty space that pushes neighbouring controls apart. No arguments are supplied.

### Line 249

```python
        summary.addWidget(text_label('Frames measured: ', 'muted'))
```

Inside `__init__`: Run this operation: `summary.addWidget`: put a control into this layout. Arguments: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'Frames measured: '`; `'muted'`.

### Line 250

```python
        self.coverage_metric = text_label('0%')
```

Inside `__init__`: Store the result in `self.coverage_metric`: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'0%'`. This is assignment, not an equality check.

### Line 251

```python
        summary.addWidget(self.coverage_metric)
```

Inside `__init__`: Run this operation: `summary.addWidget`: put a control into this layout. Arguments: `self.coverage_metric`.

### Line 252

```python
        summary.addWidget(text_label('   Scanned: ', 'muted'))
```

Inside `__init__`: Run this operation: `summary.addWidget`: put a control into this layout. Arguments: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'   Scanned: '`; `'muted'`.

### Line 253

```python
        self.time_metric = text_label('0:00')
```

Inside `__init__`: Store the result in `self.time_metric`: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'0:00'`. This is assignment, not an equality check.

### Line 254

```python
        summary.addWidget(self.time_metric)
```

Inside `__init__`: Run this operation: `summary.addWidget`: put a control into this layout. Arguments: `self.time_metric`.

### Line 255

```python
        left.addLayout(summary)
```

Inside `__init__`: Run this operation: `left.addLayout`: put another layout into this layout. Arguments: `summary`.

### Line 256

```python
        self.canvas = VideoCanvas()
```

Inside `__init__`: Store the result in `self.canvas`: `VideoCanvas`: call this function with the supplied arguments. No arguments are supplied. This is assignment, not an equality check.

### Line 257

```python
        self.canvas.point_added.connect(self.correct_points)
```

Inside `__init__`: Run this operation: `self.canvas.point_added.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.correct_points`.

### Line 258

```python
        left.addWidget(self.canvas, 5)
```

Inside `__init__`: Run this operation: `left.addWidget`: put a control into this layout. Arguments: `self.canvas`; `5`.

### Line 259

```python
        self.chart = HeightChart()
```

Inside `__init__`: Store the result in `self.chart`: `HeightChart`: call this function with the supplied arguments. No arguments are supplied. This is assignment, not an equality check.

### Line 260

```python
        self.chart.selected.connect(self.table_select)
```

Inside `__init__`: Run this operation: `self.chart.selected.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.table_select`.

### Line 261

```python
        left.addWidget(self.chart, 1)
```

Inside `__init__`: Run this operation: `left.addWidget`: put a control into this layout. Arguments: `self.chart`; `1`.

### Line 262

```python
        self.table = QTableWidget(0, 5)
```

Inside `__init__`: Store the result in `self.table`: `QTableWidget`: construct the named Qt control or display object. Arguments: `0`; `5`. This is assignment, not an equality check.

### Line 263

```python
        self.table.setHorizontalHeaderLabels(['Run', 'Jump', 'Time', 'Height (m)', 'Status'])
```

Inside `__init__`: Run this operation: `self.table.setHorizontalHeaderLabels`: name the result-table columns. Arguments: list containing `'Run'`; `'Jump'`; `'Time'`; `'Height (m)'`; `'Status'`.

### Line 264

```python
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
```

Inside `__init__`: Run this operation: `self.table.horizontalHeader().setSectionResizeMode`: choose how table columns fill available space. Arguments: `QHeaderView.ResizeMode.Stretch`.

### Line 265

```python
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
```

Inside `__init__`: Run this operation: `self.table.setSelectionBehavior`: choose whether selection covers entire rows. Arguments: `QTableWidget.SelectionBehavior.SelectRows`.

### Line 266

```python
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
```

Inside `__init__`: Run this operation: `self.table.setSelectionMode`: limit table selection to the chosen selection rule. Arguments: `QTableWidget.SelectionMode.SingleSelection`.

### Line 267

```python
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
```

Inside `__init__`: Run this operation: `self.table.setEditTriggers`: choose whether users can edit table cells directly. Arguments: `QTableWidget.EditTrigger.NoEditTriggers`.

### Line 268

```python
        self.table.verticalHeader().hide()
```

Inside `__init__`: Run this operation: `self.table.verticalHeader().hide`: hide this widget. No arguments are supplied.

### Line 269

```python
        self.table.itemSelectionChanged.connect(self.show_selected)
```

Inside `__init__`: Run this operation: `self.table.itemSelectionChanged.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.show_selected`.

### Line 270

```python
        left.addWidget(self.table, 2)
```

Inside `__init__`: Run this operation: `left.addWidget`: put a control into this layout. Arguments: `self.table`; `2`.

### Line 271

```python
        panel = QFrame()
```

Inside `__init__`: Store the result in `panel`: `QFrame`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 272

```python
        panel.setObjectName('panel')
```

Inside `__init__`: Run this operation: `panel.setObjectName`: give the control a name used by the stylesheet selector. Arguments: `'panel'`.

### Line 273

```python
        scroll = QScrollArea()
```

Inside `__init__`: Store the result in `scroll`: `QScrollArea`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 274

```python
        scroll.setWidgetResizable(True)
```

Inside `__init__`: Run this operation: `scroll.setWidgetResizable`: let the scroll area fit its panel to the available width. Arguments: `True`.

### Line 275

```python
        scroll.setFixedWidth(340)
```

Inside `__init__`: Run this operation: `scroll.setFixedWidth`: keep this sidebar at a constant width. Arguments: `340`.

### Line 276

```python
        scroll.setFrameShape(QFrame.Shape.NoFrame)
```

Inside `__init__`: Run this operation: `scroll.setFrameShape`: choose the border style for this frame. Arguments: `QFrame.Shape.NoFrame`.

### Line 277

```python
        scroll.setWidget(panel)
```

Inside `__init__`: Run this operation: `scroll.setWidget`: put this panel inside the scrollable area. Arguments: `panel`.

### Line 278

```python
        body.addWidget(scroll)
```

Inside `__init__`: Run this operation: `body.addWidget`: put a control into this layout. Arguments: `scroll`.

### Line 279

```python
        right = QVBoxLayout(panel)
```

Inside `__init__`: Store the result in `right`: `QVBoxLayout`: construct the named Qt control or display object. Arguments: `panel`. This is assignment, not an equality check.

### Line 280

```python
        right.setContentsMargins(18, 18, 18, 18)
```

Inside `__init__`: Run this operation: `right.setContentsMargins`: set inner spacing at the left, top, right, and bottom. Arguments: `18`; `18`; `18`; `18`.

### Line 281

```python
        right.addWidget(text_label('Video', 'muted'))
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'Video'`; `'muted'`.

### Line 282

```python
        self.source = QLineEdit()
```

Inside `__init__`: Store the result in `self.source`: `QLineEdit`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 283

```python
        self.source.setPlaceholderText('Choose video or paste direct link')
```

Inside `__init__`: Run this operation: `self.source.setPlaceholderText`: show a hint while the input is empty. Arguments: `'Choose video or paste direct link'`.

### Line 284

```python
        self.source.setToolTip('You can also drop a local video onto the window.')
```

Inside `__init__`: Run this operation: `self.source.setToolTip`: set the explanatory text shown when the pointer pauses over a control. Arguments: `'You can also drop a local video onto the window.'`.

### Line 285

```python
        right.addWidget(self.source)
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `self.source`.

### Line 286

```python
        row = QHBoxLayout()
```

Inside `__init__`: Store the result in `row`: `QHBoxLayout`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 287

```python
        row.addWidget(button('Browse video', self.browse))
```

Inside `__init__`: Run this operation: `row.addWidget`: put a control into this layout. Arguments: `button`: create a Qt button and connect its clicked signal to an action. Arguments: `'Browse video'`; `self.browse`.

### Line 288

```python
        row.addWidget(button('Open session', self.open_session))
```

Inside `__init__`: Run this operation: `row.addWidget`: put a control into this layout. Arguments: `button`: create a Qt button and connect its clicked signal to an action. Arguments: `'Open session'`; `self.open_session`.

### Line 289

```python
        right.addLayout(row)
```

Inside `__init__`: Run this operation: `right.addLayout`: put another layout into this layout. Arguments: `row`.

### Line 290

```python
        scan_options = QWidget()
```

Inside `__init__`: Store the result in `scan_options`: `QWidget`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 291

```python
        options = QVBoxLayout(scan_options)
```

Inside `__init__`: Store the result in `options`: `QVBoxLayout`: construct the named Qt control or display object. Arguments: `scan_options`. This is assignment, not an equality check.

### Line 292

```python
        options.setContentsMargins(0, 0, 0, 0)
```

Inside `__init__`: Run this operation: `options.setContentsMargins`: set inner spacing at the left, top, right, and bottom. Arguments: `0`; `0`; `0`; `0`.

### Line 293

```python
        self.disclosure(right, 'Scan options', scan_options)
```

Inside `__init__`: Run this operation: `self.disclosure`: hide secondary controls until their small arrow button is opened. Arguments: `right`; `'Scan options'`; `scan_options`.

### Line 294

```python
        options.addWidget(text_label('Seconds. End 0 scans the whole video.', 'muted'))
```

Inside `__init__`: Run this operation: `options.addWidget`: put a control into this layout. Arguments: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'Seconds. End 0 scans the whole video.'`; `'muted'`.

### Line 295

```python
        row = QHBoxLayout()
```

Inside `__init__`: Store the result in `row`: `QHBoxLayout`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 296

```python
        self.start = self.spin(row, 0, 999999, 'Start ')
```

Inside `__init__`: Store the result in `self.start`: `self.spin`: create a bounded decimal input and add it to the supplied layout. Arguments: `row`; `0`; `999999`; `'Start '`. This is assignment, not an equality check.

### Line 297

```python
        self.end = self.spin(row, 0, 999999, 'End ')
```

Inside `__init__`: Store the result in `self.end`: `self.spin`: create a bounded decimal input and add it to the supplied layout. Arguments: `row`; `0`; `999999`; `'End '`. This is assignment, not an equality check.

### Line 298

```python
        options.addLayout(row)
```

Inside `__init__`: Run this operation: `options.addLayout`: put another layout into this layout. Arguments: `row`.

### Line 299

```python
        self.rate = QComboBox()
```

Inside `__init__`: Store the result in `self.rate`: `QComboBox`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 300

```python
        for rate in (2, 4, 6, 10):
```

Inside `__init__`: Repeat the following indented block for each `rate` from tuple containing `2`; `4`; `6`; `10`. Tuple targets unpack each loop item.

### Line 301

```python
            self.rate.addItem(f'{rate} samples / second', rate)
```

Inside `__init__`: Run this operation: `self.rate.addItem`: add a visible choice and its stored sample-rate value. Arguments: formatted text `f'{rate} samples / second'`. Inserted values: rate; `rate`.

### Line 302

```python
        self.rate.setCurrentIndex(0)
```

Inside `__init__`: Run this operation: `self.rate.setCurrentIndex`: select a combo-box entry by zero-based position. Arguments: `0`.

### Line 303

```python
        options.addWidget(self.rate)
```

Inside `__init__`: Run this operation: `options.addWidget`: put a control into this layout. Arguments: `self.rate`.

### Line 304

```python
        self.run_button = button('Scan video', self.start_analysis, 'primary')
```

Inside `__init__`: Store the result in `self.run_button`: `button`: create a Qt button and connect its clicked signal to an action. Arguments: `'Scan video'`; `self.start_analysis`; `'primary'`. This is assignment, not an equality check.

### Line 305

```python
        right.addWidget(self.run_button)
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `self.run_button`.

### Line 306

```python
        self.stop_button = button('Stop scan', self.stop_analysis)
```

Inside `__init__`: Store the result in `self.stop_button`: `button`: create a Qt button and connect its clicked signal to an action. Arguments: `'Stop scan'`; `self.stop_analysis`. This is assignment, not an equality check.

### Line 307

```python
        self.stop_button.setEnabled(False)
```

Inside `__init__`: Run this operation: `self.stop_button.setEnabled`: enable or disable this control. Arguments: `False`.

### Line 308

```python
        right.addWidget(self.stop_button)
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `self.stop_button`.

### Line 309

```python
        self.progress = QProgressBar()
```

Inside `__init__`: Store the result in `self.progress`: `QProgressBar`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 310

```python
        self.progress.setTextVisible(False)
```

Inside `__init__`: Run this operation: `self.progress.setTextVisible`: choose whether the progress bar prints its percentage. Arguments: `False`.

### Line 311

```python
        right.addWidget(self.progress)
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `self.progress`.

### Line 312

```python
        self.status = text_label('Ready. Choose a video to start.', 'muted')
```

Inside `__init__`: Store the result in `self.status`: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'Ready. Choose a video to start.'`; `'muted'`. This is assignment, not an equality check.

### Line 313

```python
        right.addWidget(self.status)
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `self.status`.

### Line 314

```python
        right.addWidget(text_label('Selected jump', 'muted'))
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'Selected jump'`; `'muted'`.

### Line 315

```python
        self.details = text_label('Select a result to inspect its hip and lip marks.', 'muted')
```

Inside `__init__`: Store the result in `self.details`: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'Select a result to inspect its hip and lip marks.'`; `'muted'`. This is assignment, not an equality check.

### Line 316

```python
        right.addWidget(self.details)
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `self.details`.

### Line 317

```python
        self.correct_button = button('Correct points', self.start_correction)
```

Inside `__init__`: Store the result in `self.correct_button`: `button`: create a Qt button and connect its clicked signal to an action. Arguments: `'Correct points'`; `self.start_correction`. This is assignment, not an equality check.

### Line 318

```python
        right.addWidget(self.correct_button)
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `self.correct_button`.

### Line 319

```python
        row = QHBoxLayout()
```

Inside `__init__`: Store the result in `row`: `QHBoxLayout`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 320

```python
        self.manual_time = self.spin(row, 0, 999999, 'Time ')
```

Inside `__init__`: Store the result in `self.manual_time`: `self.spin`: create a bounded decimal input and add it to the supplied layout. Arguments: `row`; `0`; `999999`; `'Time '`. This is assignment, not an equality check.

### Line 321

```python
        row.addWidget(button('Add missed jump', self.add_manual))
```

Inside `__init__`: Run this operation: `row.addWidget`: put a control into this layout. Arguments: `button`: create a Qt button and connect its clicked signal to an action. Arguments: `'Add missed jump'`; `self.add_manual`.

### Line 322

```python
        right.addLayout(row)
```

Inside `__init__`: Run this operation: `right.addLayout`: put another layout into this layout. Arguments: `row`.

### Line 323

```python
        self.height_metric = text_label('Needs calibration', 'metric')
```

Inside `__init__`: Store the result in `self.height_metric`: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'Needs calibration'`; `'metric'`. This is assignment, not an equality check.

### Line 324

```python
        right.addWidget(self.height_metric)
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `self.height_metric`.

### Line 325

```python
        right.addWidget(text_label('Known vertical length near this jump', 'muted'))
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'Known vertical length near this jump'`; `'muted'`.

### Line 326

```python
        row = QHBoxLayout()
```

Inside `__init__`: Store the result in `row`: `QHBoxLayout`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 327

```python
        self.reference_length = self.spin(row, 0.01, 100, '')
```

Inside `__init__`: Store the result in `self.reference_length`: `self.spin`: create a bounded decimal input and add it to the supplied layout. Arguments: `row`; `0.01`; `100`; `''`. This is assignment, not an equality check.

### Line 328

```python
        self.reference_length.setValue(6.7)
```

Inside `__init__`: Run this operation: `self.reference_length.setValue`: set the numeric input or progress value. Arguments: `6.7`.

### Line 329

```python
        row.addWidget(text_label('metres', 'muted'))
```

Inside `__init__`: Run this operation: `row.addWidget`: put a control into this layout. Arguments: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'metres'`; `'muted'`.

### Line 330

```python
        right.addLayout(row)
```

Inside `__init__`: Run this operation: `right.addLayout`: put another layout into this layout. Arguments: `row`.

### Line 331

```python
        right.addWidget(button('Calibrate this jump', self.start_calibration))
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `button`: create a Qt button and connect its clicked signal to an action. Arguments: `'Calibrate this jump'`; `self.start_calibration`.

### Line 332

```python
        row = QHBoxLayout()
```

Inside `__init__`: Store the result in `row`: `QHBoxLayout`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 333

```python
        row.addWidget(button('Mark reviewed', self.mark_reviewed))
```

Inside `__init__`: Run this operation: `row.addWidget`: put a control into this layout. Arguments: `button`: create a Qt button and connect its clicked signal to an action. Arguments: `'Mark reviewed'`; `self.mark_reviewed`.

### Line 334

```python
        row.addWidget(button('Exclude', self.exclude, 'danger'))
```

Inside `__init__`: Run this operation: `row.addWidget`: put a control into this layout. Arguments: `button`: create a Qt button and connect its clicked signal to an action. Arguments: `'Exclude'`; `self.exclude`; `'danger'`.

### Line 335

```python
        right.addLayout(row)
```

Inside `__init__`: Run this operation: `right.addLayout`: put another layout into this layout. Arguments: `row`.

### Line 336

```python
        right.addWidget(text_label('6.7 m is the supplied wall height. Use it only if both ends of that vertical height are visible at the rider\'s depth. Never use the curved wall surface as the reference.', 'muted'))
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `"6.7 m is the supplied wall height. Use it only if both ends of that vertical height are visible at the rider's depth. Never use the curved wall surface as the reference."`; `'muted'`.

### Line 337

```python
        pipe_info = text_label('Pipe: 6.7 m high, 160 m long, 22 m wide. Slope: 18 degrees. Wall inclination: 81 degrees. These dimensions still need visible reference points for metre calibration.', 'muted')
```

Inside `__init__`: Store the result in `pipe_info`: `text_label`: create a wrapping Qt text label and optionally give it a named style. Arguments: `'Pipe: 6.7 m high, 160 m long, 22 m wide. Slope: 18 degrees. Wall inclination: 81 degrees. These dimensions still need visible reference points for metre calibration.'`; `'muted'`. This is assignment, not an equality check.

### Line 338

```python
        self.disclosure(right, 'Pipe dimensions', pipe_info)
```

Inside `__init__`: Run this operation: `self.disclosure`: hide secondary controls until their small arrow button is opened. Arguments: `right`; `'Pipe dimensions'`; `pipe_info`.

### Line 339

```python
        right.addStretch()
```

Inside `__init__`: Run this operation: `right.addStretch`: add flexible empty space that pushes neighbouring controls apart. No arguments are supplied.

### Line 340

```python
        right.addWidget(button('Export results CSV', self.export_results))
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `button`: create a Qt button and connect its clicked signal to an action. Arguments: `'Export results CSV'`; `self.export_results`.

### Line 341

```python
        right.addWidget(button('Open results folder', self.open_results))
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `button`: create a Qt button and connect its clicked signal to an action. Arguments: `'Open results folder'`; `self.open_results`.

### Line 342

```python
        right.addWidget(button('Play marked review video', self.open_review_video))
```

Inside `__init__`: Run this operation: `right.addWidget`: put a control into this layout. Arguments: `button`: create a Qt button and connect its clicked signal to an action. Arguments: `'Play marked review video'`; `self.open_review_video`.

### Line 343

```python
        guide = QTextBrowser()
```

Inside `__init__`: Store the result in `guide`: `QTextBrowser`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 344

```python
        guide.setOpenExternalLinks(True)
```

Inside `__init__`: Run this operation: `guide.setOpenExternalLinks`: allow documentation links to open in the normal browser. Arguments: `True`.

### Line 345

```python
        guide.setMarkdown((Path(__file__).parent / 'docs' / 'APP_HELP.md').read_text(encoding='utf-8'))
```

Inside `__init__`: Run this operation: `guide.setMarkdown`: render the supplied Markdown document in the help tab. Arguments: `(Path(__file__).parent / 'docs' / 'APP_HELP.md').read_text`: read a complete text file with the selected encoding. Arguments: encoding = `'utf-8'`.

### Line 346

```python
        self.tabs.addTab(guide, 'How it works')
```

Inside `__init__`: Run this operation: `self.tabs.addTab`: add a labelled page to the tab control. Arguments: `guide`; `'How it works'`.

### Line 347

```python
        self.load_recent()
```

Inside `__init__`: Run this operation: `self.load_recent`: try to reopen the last report without interrupting startup if it is absent. No arguments are supplied.

### Line 348

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 349

```python
    def disclosure(self, layout, title, content):
```

Inside `MainWindow`: Define `disclosure(self, layout, title, content)`. Its job: Keep secondary settings out of the way until the user opens them. The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 350

```python
        """Keep secondary settings out of the way until the user opens them."""
```

Inside `disclosure`: Documentation string: Keep secondary settings out of the way until the user opens them. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 351

```python
        toggle = QToolButton()
```

Inside `disclosure`: Store the result in `toggle`: `QToolButton`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 352

```python
        toggle.setText(title)
```

Inside `disclosure`: Run this operation: `toggle.setText`: replace the visible label or input text. Arguments: `title`.

### Line 353

```python
        toggle.setCheckable(True)
```

Inside `disclosure`: Run this operation: `toggle.setCheckable`: let this button keep an on or off state after a click. Arguments: `True`.

### Line 354

```python
        toggle.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
```

Inside `disclosure`: Run this operation: `toggle.setToolButtonStyle`: choose how this small button arranges its icon and text. Arguments: `Qt.ToolButtonStyle.ToolButtonTextBesideIcon`.

### Line 355

```python
        toggle.setArrowType(Qt.ArrowType.RightArrow)
```

Inside `disclosure`: Run this operation: `toggle.setArrowType`: choose the direction of this disclosure button arrow. Arguments: `Qt.ArrowType.RightArrow`.

### Line 356

```python
        toggle.toggled.connect(content.setVisible)
```

Inside `disclosure`: Run this operation: `toggle.toggled.connect`: register the function to run when this Qt signal is emitted. Arguments: `content.setVisible`.

### Line 357

```python
        toggle.toggled.connect(lambda opened: toggle.setArrowType(Qt.ArrowType.DownArrow if opened else Qt.ArrowType.RightArrow))
```

Inside `disclosure`: Run this operation: `toggle.toggled.connect`: register the function to run when this Qt signal is emitted. Arguments: a short function taking `opened` and returning `toggle.setArrowType`: choose the direction of this disclosure button arrow. Arguments: `Qt.ArrowType.DownArrow` when `opened`; otherwise `Qt.ArrowType.RightArrow`.

### Line 358

```python
        content.hide()
```

Inside `disclosure`: Run this operation: `content.hide`: hide this widget. No arguments are supplied.

### Line 359

```python
        layout.addWidget(toggle)
```

Inside `disclosure`: Run this operation: `layout.addWidget`: put a control into this layout. Arguments: `toggle`.

### Line 360

```python
        layout.addWidget(content)
```

Inside `disclosure`: Run this operation: `layout.addWidget`: put a control into this layout. Arguments: `content`.

### Line 361

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 362

```python
    def spin(self, layout, minimum, maximum, prefix):
```

Inside `MainWindow`: Define `spin(self, layout, minimum, maximum, prefix)`. Its job: create a bounded decimal input and add it to the supplied layout The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 363

```python
        control = QDoubleSpinBox()
```

Inside `spin`: Store the result in `control`: `QDoubleSpinBox`: construct the named Qt control or display object. No arguments are supplied. This is assignment, not an equality check.

### Line 364

```python
        control.setRange(minimum, maximum)
```

Inside `spin`: Run this operation: `control.setRange`: limit a numeric input to the supplied lower and upper values. Arguments: `minimum`; `maximum`.

### Line 365

```python
        control.setDecimals(2)
```

Inside `spin`: Run this operation: `control.setDecimals`: choose the displayed precision of a numeric input. Arguments: `2`.

### Line 366

```python
        control.setPrefix(prefix)
```

Inside `spin`: Run this operation: `control.setPrefix`: put fixed explanatory text before the numeric value. Arguments: `prefix`.

### Line 367

```python
        layout.addWidget(control)
```

Inside `spin`: Run this operation: `layout.addWidget`: put a control into this layout. Arguments: `control`.

### Line 368

```python
        return control
```

Inside `spin`: End this function now and send back `control`. A bare return sends None.

### Line 369

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 370

```python
    def browse(self):
```

Inside `MainWindow`: Define `browse(self)`. Its job: choose a local video with the standard file dialog The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 371

```python
        path, kind = QFileDialog.getOpenFileName(self, 'Open a video', '', 'Videos (*.mp4 *.mov *.mkv *.avi);;All files (*)')
```

Inside `browse`: Store the result in `(path, kind)`: `QFileDialog.getOpenFileName`: ask the user to select a file, returning its path and filter. Arguments: `self`; `'Open a video'`; `''`; `'Videos (*.mp4 *.mov *.mkv *.avi);;All files (*)'`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 372

```python
        if path:
```

Inside `browse`: Run the indented block only when this condition is true: `path`. Other branches handle the remaining case.

### Line 373

```python
            self.source.setText(path)
```

Inside `browse`: Run this operation: `self.source.setText`: replace the visible label or input text. Arguments: `path`.

### Line 374

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 375

```python
    def start_analysis(self):
```

Inside `MainWindow`: Define `start_analysis(self)`. Its job: validate the source and start a background analysis worker The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 376

```python
        if self.frame_worker and self.frame_worker.isRunning():
```

Inside `start_analysis`: Run the indented block only when this condition is true: `self.frame_worker` AND `self.frame_worker.isRunning`: check whether this worker thread is active. No arguments are supplied. Other branches handle the remaining case.

### Line 377

```python
            self.status.setText('Wait for the peak frame to finish loading.')
```

Inside `start_analysis`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `'Wait for the peak frame to finish loading.'`.

### Line 378

```python
            return
```

Inside `start_analysis`: End this function now and send back no explicit value. A bare return sends None.

### Line 379

```python
        source = self.source.text().strip().replace('https\\://', 'https://')
```

Inside `start_analysis`: Store the result in `source`: `self.source.text().strip().replace`: replace the target path atomically on this filesystem, or replace matching text in a string. Arguments: `'https\\://'`; `'https://'`. This is assignment, not an equality check.

### Line 380

```python
        if not source:
```

Inside `start_analysis`: Run the indented block only when this condition is true: NOT `source`. Other branches handle the remaining case.

### Line 381

```python
            self.status.setText('Choose a local video or paste a direct video link first.')
```

Inside `start_analysis`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `'Choose a local video or paste a direct video link first.'`.

### Line 382

```python
            return
```

Inside `start_analysis`: End this function now and send back no explicit value. A bare return sends None.

### Line 383

```python
        if self.worker and self.worker.isRunning():
```

Inside `start_analysis`: Run the indented block only when this condition is true: `self.worker` AND `self.worker.isRunning`: check whether this worker thread is active. No arguments are supplied. Other branches handle the remaining case.

### Line 384

```python
            return
```

Inside `start_analysis`: End this function now and send back no explicit value. A bare return sends None.

### Line 385

```python
        self.worker = AnalysisWorker(dict(source=source, start=self.start.value(), end=self.end.value(), sample_rate=self.rate.currentData()))
```

Inside `start_analysis`: Store the result in `self.worker`: `AnalysisWorker`: call this function with the supplied arguments. Arguments: `dict`: create a dictionary from the named fields. Arguments: source = `source`; start = `self.start.value`: read the current numeric input value. No arguments are supplied; end = `self.end.value`: read the current numeric input value. No arguments are supplied; sample_rate = `self.rate.currentData`: read the stored value behind the selected combo-box text. No arguments are supplied. This is assignment, not an equality check.

### Line 386

```python
        self.worker.progress.connect(self.update_progress)
```

Inside `start_analysis`: Run this operation: `self.worker.progress.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.update_progress`.

### Line 387

```python
        self.worker.preview.connect(self.canvas.show_frame)
```

Inside `start_analysis`: Run this operation: `self.worker.preview.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.canvas.show_frame`.

### Line 388

```python
        self.worker.result.connect(self.receive_report)
```

Inside `start_analysis`: Run this operation: `self.worker.result.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.receive_report`.

### Line 389

```python
        self.worker.failed.connect(self.show_error)
```

Inside `start_analysis`: Run this operation: `self.worker.failed.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.show_error`.

### Line 390

```python
        self.worker.finished.connect(self.analysis_finished)
```

Inside `start_analysis`: Run this operation: `self.worker.finished.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.analysis_finished`.

### Line 391

```python
        self.run_button.setEnabled(False)
```

Inside `start_analysis`: Run this operation: `self.run_button.setEnabled`: enable or disable this control. Arguments: `False`.

### Line 392

```python
        self.stop_button.setEnabled(True)
```

Inside `start_analysis`: Run this operation: `self.stop_button.setEnabled`: enable or disable this control. Arguments: `True`.

### Line 393

```python
        self.correct_button.setEnabled(False)
```

Inside `start_analysis`: Run this operation: `self.correct_button.setEnabled`: enable or disable this control. Arguments: `False`.

### Line 394

```python
        self.table.setEnabled(False)
```

Inside `start_analysis`: Run this operation: `self.table.setEnabled`: enable or disable this control. Arguments: `False`.

### Line 395

```python
        self.canvas.correcting = False
```

Inside `start_analysis`: Store the result in `self.canvas.correcting`: `False`. This is assignment, not an equality check.

### Line 396

```python
        self.progress.setValue(0)
```

Inside `start_analysis`: Run this operation: `self.progress.setValue`: set the numeric input or progress value. Arguments: `0`.

### Line 397

```python
        self.status.setText('Opening video and preparing the detector...')
```

Inside `start_analysis`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `'Opening video and preparing the detector...'`.

### Line 398

```python
        self.worker.start()
```

Inside `start_analysis`: Run this operation: `self.worker.start`: start the worker thread; Qt then calls its run method. No arguments are supplied.

### Line 399

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 400

```python
    def update_progress(self, data):
```

Inside `MainWindow`: Define `update_progress(self, data)`. Its job: provide this reusable operation The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 401

```python
        self.progress.setValue(round(data.get('percent', 0)))
```

Inside `update_progress`: Run this operation: `self.progress.setValue`: set the numeric input or progress value. Arguments: `round`: round a number to the requested precision. Arguments: `data.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'percent'`; `0`.

### Line 402

```python
        seconds = data.get('time', 0)
```

Inside `update_progress`: Store the result in `seconds`: `data.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'time'`; `0`. This is assignment, not an equality check.

### Line 403

```python
        self.time_metric.setText(f'{int(seconds) // 60}:{int(seconds) % 60:02}')
```

Inside `update_progress`: Run this operation: `self.time_metric.setText`: replace the visible label or input text. Arguments: formatted text `f'{int(seconds) // 60}:{int(seconds) % 60:02}'`. Inserted values: int(seconds) // 60; int(seconds) % 60, format f'02'.

### Line 404

```python
        self.coverage_metric.setText(f"{100 * data.get('measured', 0) / max(1, data.get('samples', 0)):.0f}%")
```

Inside `update_progress`: Run this operation: `self.coverage_metric.setText`: replace the visible label or input text. Arguments: formatted text `f"{100 * data.get('measured', 0) / max(1, data.get('samples', 0)):.0f}%"`. Inserted values: 100 * data.get('measured', 0) / max(1, data.get('samples', 0)), format f'.0f'.

### Line 405

```python
        self.status.setText(data.get('message', '') + (f"\nAbout {data['remaining'] / 60:.1f} minutes remaining" if 'remaining' in data else ''))
```

Inside `update_progress`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: (`data.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'message'`; `''` plus formatted text `f"\nAbout {data['remaining'] / 60:.1f} minutes remaining"`. Inserted values: data['remaining'] / 60, format f'.1f' when `'remaining'` is in `data`; otherwise `''`).

### Line 406

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 407

```python
    def stop_analysis(self):
```

Inside `MainWindow`: Define `stop_analysis(self)`. Its job: request an orderly stop and keep the partial session The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 408

```python
        if self.worker and self.worker.isRunning():
```

Inside `stop_analysis`: Run the indented block only when this condition is true: `self.worker` AND `self.worker.isRunning`: check whether this worker thread is active. No arguments are supplied. Other branches handle the remaining case.

### Line 409

```python
            self.worker.requestInterruption()
```

Inside `stop_analysis`: Run this operation: `self.worker.requestInterruption`: set the worker's cooperative stop flag. No arguments are supplied.

### Line 410

```python
            self.status.setText('Stopping after the current video read. Saving partial results...')
```

Inside `stop_analysis`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `'Stopping after the current video read. Saving partial results...'`.

### Line 411

```python
            self.stop_button.setEnabled(False)
```

Inside `stop_analysis`: Run this operation: `self.stop_button.setEnabled`: enable or disable this control. Arguments: `False`.

### Line 412

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 413

```python
    def receive_report(self, report):
```

Inside `MainWindow`: Define `receive_report(self, report)`. Its job: replace the displayed session and refresh its candidates and metrics The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 414

```python
        self.report = report
```

Inside `receive_report`: Store the result in `self.report`: `report`. This is assignment, not an equality check.

### Line 415

```python
        self.source.setText(report['source'])
```

Inside `receive_report`: Run this operation: `self.source.setText`: replace the visible label or input text. Arguments: `report['source']`.

### Line 416

```python
        self.refresh_results()
```

Inside `receive_report`: Run this operation: `self.refresh_results`: rebuild table rows and update the candidate count, coverage, and timeline. No arguments are supplied.

### Line 417

```python
        self.progress.setValue(100 if report['complete'] else 0)
```

Inside `receive_report`: Run this operation: `self.progress.setValue`: set the numeric input or progress value. Arguments: `100` when `report['complete']`; otherwise `0`.

### Line 418

```python
        self.status.setText(f"{report['state'].replace('_', ' ').title()}. {len(report['jumps'])} candidates. Review before using results.")
```

Inside `receive_report`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: formatted text `f"{report['state'].replace('_', ' ').title()}. {len(report['jumps'])} candidates. Review before using results."`. Inserted values: report['state'].replace('_', ' ').title(); len(report['jumps']).

### Line 419

```python
        self.save_recent()
```

Inside `receive_report`: Run this operation: `self.save_recent`: save a small pointer to the last opened report. No arguments are supplied.

### Line 420

```python
        if report['jumps']:
```

Inside `receive_report`: Run the indented block only when this condition is true: `report['jumps']`. Other branches handle the remaining case.

### Line 421

```python
            self.table.selectRow(0)
```

Inside `receive_report`: Run this operation: `self.table.selectRow`: select the requested result row. Arguments: `0`.

### Line 422

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 423

```python
    def analysis_finished(self):
```

Inside `MainWindow`: Define `analysis_finished(self)`. Its job: restore controls after the worker has ended and finish a pending close The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 424

```python
        self.run_button.setEnabled(True)
```

Inside `analysis_finished`: Run this operation: `self.run_button.setEnabled`: enable or disable this control. Arguments: `True`.

### Line 425

```python
        self.stop_button.setEnabled(False)
```

Inside `analysis_finished`: Run this operation: `self.stop_button.setEnabled`: enable or disable this control. Arguments: `False`.

### Line 426

```python
        self.correct_button.setEnabled(True)
```

Inside `analysis_finished`: Run this operation: `self.correct_button.setEnabled`: enable or disable this control. Arguments: `True`.

### Line 427

```python
        self.table.setEnabled(True)
```

Inside `analysis_finished`: Run this operation: `self.table.setEnabled`: enable or disable this control. Arguments: `True`.

### Line 428

```python
        if self.close_pending:
```

Inside `analysis_finished`: Run the indented block only when this condition is true: `self.close_pending`. Other branches handle the remaining case.

### Line 429

```python
            self.close()
```

Inside `analysis_finished`: Run this operation: `self.close`: request that the window close. No arguments are supplied.

### Line 430

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 431

```python
    def refresh_results(self):
```

Inside `MainWindow`: Define `refresh_results(self)`. Its job: rebuild table rows and update the candidate count, coverage, and timeline The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 432

```python
        report = self.report
```

Inside `refresh_results`: Store the result in `report`: `self.report`. This is assignment, not an equality check.

### Line 433

```python
        self.table.blockSignals(True)
```

Inside `refresh_results`: Run this operation: `self.table.blockSignals`: temporarily suppress selection callbacks while rebuilding table data. Arguments: `True`.

### Line 434

```python
        self.table.setRowCount(len(report['jumps']))
```

Inside `refresh_results`: Run this operation: `self.table.setRowCount`: resize the table to the number of candidate rows. Arguments: `len`: count items. Arguments: `report['jumps']`.

### Line 435

```python
        for row, jump in enumerate(report['jumps']):
```

Inside `refresh_results`: Repeat the following indented block for each `(row, jump)` from `enumerate`: provide both each item's index and its value. Arguments: `report['jumps']`. Tuple targets unpack each loop item.

### Line 436

```python
            state = 'Excluded' if jump['excluded'] else ('Reviewed' if jump['reviewed'] else 'Needs review')
```

Inside `refresh_results`: Store the result in `state`: `'Excluded'` when `jump['excluded']`; otherwise `'Reviewed'` when `jump['reviewed']`; otherwise `'Needs review'`. This is assignment, not an equality check.

### Line 437

```python
            values = [str(jump.get('run', '?')), str(jump.get('jump_in_run', jump['id'])), f"{jump['peak_time']:.2f}s", 'Calibrate' if jump['height_m'] is None else f"{jump['height_m']:.2f} m", state]
```

Inside `refresh_results`: Store the result in `values`: list containing `str`: convert a value to text. Arguments: `jump.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'run'`; `'?'`; `str`: convert a value to text. Arguments: `jump.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'jump_in_run'`; `jump['id']`; formatted text `f"{jump['peak_time']:.2f}s"`. Inserted values: jump['peak_time'], format f'.2f'; `'Calibrate'` when `jump['height_m']` is the same object as `None`; otherwise formatted text `f"{jump['height_m']:.2f} m"`. Inserted values: jump['height_m'], format f'.2f'; `state`. This is assignment, not an equality check.

### Line 438

```python
            for column, value in enumerate(values):
```

Inside `refresh_results`: Repeat the following indented block for each `(column, value)` from `enumerate`: provide both each item's index and its value. Arguments: `values`. Tuple targets unpack each loop item.

### Line 439

```python
                self.table.setItem(row, column, QTableWidgetItem(value))
```

Inside `refresh_results`: Run this operation: `self.table.setItem`: put the supplied text item into one table cell. Arguments: `row`; `column`; `QTableWidgetItem`: construct the named Qt control or display object. Arguments: `value`.

### Line 440

```python
        self.table.blockSignals(False)
```

Inside `refresh_results`: Run this operation: `self.table.blockSignals`: temporarily suppress selection callbacks while rebuilding table data. Arguments: `False`.

### Line 441

```python
        self.candidate_metric.setText(str(sum(not jump['excluded'] for jump in report['jumps'])))
```

Inside `refresh_results`: Run this operation: `self.candidate_metric.setText`: replace the visible label or input text. Arguments: `str`: convert a value to text. Arguments: `sum`: add values; adding booleans counts True results. Arguments: produce NOT `jump['excluded']`, for each jump in `report['jumps']`.

### Line 442

```python
        measured = sum(sample['height_px'] is not None for sample in report['samples'])
```

Inside `refresh_results`: Store the result in `measured`: `sum`: add values; adding booleans counts True results. Arguments: produce `sample['height_px']` is not the same object as `None`, for each sample in `report['samples']`. This is assignment, not an equality check.

### Line 443

```python
        self.coverage_metric.setText(f"{100 * measured / max(1, len(report['samples'])):.0f}%")
```

Inside `refresh_results`: Run this operation: `self.coverage_metric.setText`: replace the visible label or input text. Arguments: formatted text `f"{100 * measured / max(1, len(report['samples'])):.0f}%"`. Inserted values: 100 * measured / max(1, len(report['samples'])), format f'.0f'.

### Line 444

```python
        last_time = max((sample['time'] for sample in report['samples']), default=report['start'])
```

Inside `refresh_results`: Store the result in `last_time`: `max`: choose the largest value, or the item with the largest key. Arguments: produce `sample['time']`, for each sample in `report['samples']`; default = `report['start']`. This is assignment, not an equality check.

### Line 445

```python
        self.time_metric.setText(f'{int(last_time) // 60}:{int(last_time) % 60:02}')
```

Inside `refresh_results`: Run this operation: `self.time_metric.setText`: replace the visible label or input text. Arguments: formatted text `f'{int(last_time) // 60}:{int(last_time) % 60:02}'`. Inserted values: int(last_time) // 60; int(last_time) % 60, format f'02'.

### Line 446

```python
        self.chart.report = report
```

Inside `refresh_results`: Store the result in `self.chart.report`: `report`. This is assignment, not an equality check.

### Line 447

```python
        self.chart.update()
```

Inside `refresh_results`: Run this operation: `self.chart.update`: replace or add the supplied named fields. No arguments are supplied.

### Line 448

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 449

```python
    def selected_jump(self):
```

Inside `MainWindow`: Define `selected_jump(self)`. Its job: look up the candidate belonging to the selected table row The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 450

```python
        row = self.table.currentRow()
```

Inside `selected_jump`: Store the result in `row`: `self.table.currentRow`: read the selected row index, or -1 if no row is selected. No arguments are supplied. This is assignment, not an equality check.

### Line 451

```python
        return self.report['jumps'][row] if self.report and 0 <= row < len(self.report['jumps']) else None
```

Inside `selected_jump`: End this function now and send back `self.report['jumps'][row]` when `self.report` AND `0` is at most `row` and is less than `len`: count items. Arguments: `self.report['jumps']`; otherwise `None`. A bare return sends None.

### Line 452

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 453

```python
    def table_select(self, index):
```

Inside `MainWindow`: Define `table_select(self, index)`. Its job: select a table row from a timeline click The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 454

```python
        self.table.selectRow(index)
```

Inside `table_select`: Run this operation: `self.table.selectRow`: select the requested result row. Arguments: `index`.

### Line 455

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 456

```python
    def show_selected(self):
```

Inside `MainWindow`: Define `show_selected(self)`. Its job: display the selected candidate's evidence and saved image The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 457

```python
        jump = self.selected_jump()
```

Inside `show_selected`: Store the result in `jump`: `self.selected_jump`: look up the candidate belonging to the selected table row. No arguments are supplied. This is assignment, not an equality check.

### Line 458

```python
        if not jump:
```

Inside `show_selected`: Run the indented block only when this condition is true: NOT `jump`. Other branches handle the remaining case.

### Line 459

```python
            return
```

Inside `show_selected`: End this function now and send back no explicit value. A bare return sends None.

### Line 460

```python
        self.canvas.correcting = False
```

Inside `show_selected`: Store the result in `self.canvas.correcting`: `False`. This is assignment, not an equality check.

### Line 461

```python
        self.canvas.points = []
```

Inside `show_selected`: Store the result in `self.canvas.points`: an empty list `[]`. This is assignment, not an equality check.

### Line 462

```python
        self.height_metric.setText('Needs calibration' if jump['height_m'] is None else f"{jump['height_m']:.2f} m")
```

Inside `show_selected`: Run this operation: `self.height_metric.setText`: replace the visible label or input text. Arguments: `'Needs calibration'` when `jump['height_m']` is the same object as `None`; otherwise formatted text `f"{jump['height_m']:.2f} m"`. Inserted values: jump['height_m'], format f'.2f'.

### Line 463

```python
        self.details.setText(f"Run {jump.get('run', '?')}, jump {jump.get('jump_in_run', jump['id'])} at {jump['peak_time']:.2f}s\nImage gap: {jump['height_px']:.1f} px\n" + '\n'.join(jump['reasons']))
```

Inside `show_selected`: Run this operation: `self.details.setText`: replace the visible label or input text. Arguments: (formatted text `f"Run {jump.get('run', '?')}, jump {jump.get('jump_in_run', jump['id'])} at {jump['peak_time']:.2f}s\nImage gap: {jump['height_px']:.1f} px\n"`. Inserted values: jump.get('run', '?'); jump.get('jump_in_run', jump['id']); jump['peak_time'], format f'.2f'; jump['height_px'], format f'.1f' plus `'\n'.join`: call this function with the supplied arguments. Arguments: `jump['reasons']`).

### Line 464

```python
        snapshot = Path(self.report['folder']) / jump.get('snapshot', 'missing.jpg')
```

Inside `show_selected`: Store the result in `snapshot`: (`Path`: create a filesystem path object. Arguments: `self.report['folder']` divided by `jump.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'snapshot'`; `'missing.jpg'`). This is assignment, not an equality check.

### Line 465

```python
        if snapshot.exists():
```

Inside `show_selected`: Run the indented block only when this condition is true: `snapshot.exists`: check whether this path currently exists. No arguments are supplied. Other branches handle the remaining case.

### Line 466

```python
            image = cv2.imread(str(snapshot))
```

Inside `show_selected`: Store the result in `image`: `cv2.imread`: load an image as a BGR pixel array. Arguments: `str`: convert a value to text. Arguments: `snapshot`. This is assignment, not an equality check.

### Line 467

```python
            if image is not None:
```

Inside `show_selected`: Run the indented block only when this condition is true: `image` is not the same object as `None`. Other branches handle the remaining case.

### Line 468

```python
                self.canvas.show_frame(image)
```

Inside `show_selected`: Run this operation: `self.canvas.show_frame`: copy a video frame, convert its colours, and fit it inside the canvas. Arguments: `image`.

### Line 469

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 470

```python
    def start_correction(self):
```

Inside `MainWindow`: Define `start_correction(self)`. Its job: load the selected original peak frame in a background reader The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 471

```python
        jump = self.selected_jump()
```

Inside `start_correction`: Store the result in `jump`: `self.selected_jump`: look up the candidate belonging to the selected table row. No arguments are supplied. This is assignment, not an equality check.

### Line 472

```python
        if not jump or (self.frame_worker and self.frame_worker.isRunning()):
```

Inside `start_correction`: Run the indented block only when this condition is true: NOT `jump` OR `self.frame_worker` AND `self.frame_worker.isRunning`: check whether this worker thread is active. No arguments are supplied. Other branches handle the remaining case.

### Line 473

```python
            return
```

Inside `start_correction`: End this function now and send back no explicit value. A bare return sends None.

### Line 474

```python
        self.status.setText('Loading the original peak frame for correction...')
```

Inside `start_correction`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `'Loading the original peak frame for correction...'`.

### Line 475

```python
        self.correct_button.setEnabled(False)
```

Inside `start_correction`: Run this operation: `self.correct_button.setEnabled`: enable or disable this control. Arguments: `False`.

### Line 476

```python
        self.frame_worker = FrameWorker(self.report['source'], jump['frame'])
```

Inside `start_correction`: Store the result in `self.frame_worker`: `FrameWorker`: call this function with the supplied arguments. Arguments: `self.report['source']`; `jump['frame']`. This is assignment, not an equality check.

### Line 477

```python
        self.correction_jump = jump
```

Inside `start_correction`: Store the result in `self.correction_jump`: `jump`. This is assignment, not an equality check.

### Line 478

```python
        self.pending_manual = None
```

Inside `start_correction`: Store the result in `self.pending_manual`: `None`. This is assignment, not an equality check.

### Line 479

```python
        self.correction_mode = 'points'
```

Inside `start_correction`: Store the result in `self.correction_mode`: `'points'`. This is assignment, not an equality check.

### Line 480

```python
        self.table.setEnabled(False)
```

Inside `start_correction`: Run this operation: `self.table.setEnabled`: enable or disable this control. Arguments: `False`.

### Line 481

```python
        self.frame_worker.loaded.connect(self.begin_correction)
```

Inside `start_correction`: Run this operation: `self.frame_worker.loaded.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.begin_correction`.

### Line 482

```python
        self.frame_worker.failed.connect(self.show_error)
```

Inside `start_correction`: Run this operation: `self.frame_worker.failed.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.show_error`.

### Line 483

```python
        self.frame_worker.finished.connect(self.correction_loaded)
```

Inside `start_correction`: Run this operation: `self.frame_worker.finished.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.correction_loaded`.

### Line 484

```python
        self.frame_worker.start()
```

Inside `start_correction`: Run this operation: `self.frame_worker.start`: start the worker thread; Qt then calls its run method. No arguments are supplied.

### Line 485

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 486

```python
    def add_manual(self):
```

Inside `MainWindow`: Define `add_manual(self)`. Its job: load an explicitly chosen source time for a missed-jump measurement The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 487

```python
        if not self.report or (self.worker and self.worker.isRunning()) or (self.frame_worker and self.frame_worker.isRunning()):
```

Inside `add_manual`: Run the indented block only when this condition is true: NOT `self.report` OR `self.worker` AND `self.worker.isRunning`: check whether this worker thread is active. No arguments are supplied OR `self.frame_worker` AND `self.frame_worker.isRunning`: check whether this worker thread is active. No arguments are supplied. Other branches handle the remaining case.

### Line 488

```python
            self.status.setText('Finish analysis or open a session before adding a missed jump.')
```

Inside `add_manual`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `'Finish analysis or open a session before adding a missed jump.'`.

### Line 489

```python
            return
```

Inside `add_manual`: End this function now and send back no explicit value. A bare return sends None.

### Line 490

```python
        second = self.manual_time.value()
```

Inside `add_manual`: Store the result in `second`: `self.manual_time.value`: read the current numeric input value. No arguments are supplied. This is assignment, not an equality check.

### Line 491

```python
        if not self.report['start'] <= second < self.report['end']:
```

Inside `add_manual`: Run the indented block only when this condition is true: NOT `self.report['start']` is at most `second` and is less than `self.report['end']`. Other branches handle the remaining case.

### Line 492

```python
            self.status.setText('Choose a time inside this session range.')
```

Inside `add_manual`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `'Choose a time inside this session range.'`.

### Line 493

```python
            return
```

Inside `add_manual`: End this function now and send back no explicit value. A bare return sends None.

### Line 494

```python
        self.correction_mode = 'points'
```

Inside `add_manual`: Store the result in `self.correction_mode`: `'points'`. This is assignment, not an equality check.

### Line 495

```python
        self.pending_manual = dict(time=second, frame=round(second * self.report['fps']))
```

Inside `add_manual`: Store the result in `self.pending_manual`: `dict`: create a dictionary from the named fields. Arguments: time = `second`; frame = `round`: round a number to the requested precision. Arguments: (`second` times `self.report['fps']`). This is assignment, not an equality check.

### Line 496

```python
        self.correction_jump = None
```

Inside `add_manual`: Store the result in `self.correction_jump`: `None`. This is assignment, not an equality check.

### Line 497

```python
        self.frame_worker = FrameWorker(self.report['source'], self.pending_manual['frame'])
```

Inside `add_manual`: Store the result in `self.frame_worker`: `FrameWorker`: call this function with the supplied arguments. Arguments: `self.report['source']`; `self.pending_manual['frame']`. This is assignment, not an equality check.

### Line 498

```python
        self.frame_worker.loaded.connect(self.begin_correction)
```

Inside `add_manual`: Run this operation: `self.frame_worker.loaded.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.begin_correction`.

### Line 499

```python
        self.frame_worker.failed.connect(self.show_error)
```

Inside `add_manual`: Run this operation: `self.frame_worker.failed.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.show_error`.

### Line 500

```python
        self.frame_worker.finished.connect(self.correction_loaded)
```

Inside `add_manual`: Run this operation: `self.frame_worker.finished.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.correction_loaded`.

### Line 501

```python
        self.correct_button.setEnabled(False)
```

Inside `add_manual`: Run this operation: `self.correct_button.setEnabled`: enable or disable this control. Arguments: `False`.

### Line 502

```python
        self.table.setEnabled(False)
```

Inside `add_manual`: Run this operation: `self.table.setEnabled`: enable or disable this control. Arguments: `False`.

### Line 503

```python
        self.frame_worker.start()
```

Inside `add_manual`: Run this operation: `self.frame_worker.start`: start the worker thread; Qt then calls its run method. No arguments are supplied.

### Line 504

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 505

```python
    def correction_loaded(self):
```

Inside `MainWindow`: Define `correction_loaded(self)`. Its job: restore review controls once frame loading has ended The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 506

```python
        self.correct_button.setEnabled(True)
```

Inside `correction_loaded`: Run this operation: `self.correct_button.setEnabled`: enable or disable this control. Arguments: `True`.

### Line 507

```python
        self.table.setEnabled(True)
```

Inside `correction_loaded`: Run this operation: `self.table.setEnabled`: enable or disable this control. Arguments: `True`.

### Line 508

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 509

```python
    def begin_correction(self, frame):
```

Inside `MainWindow`: Define `begin_correction(self, frame)`. Its job: display the original frame and begin collecting three measurement points The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 510

```python
        self.raw_frame = frame
```

Inside `begin_correction`: Store the result in `self.raw_frame`: `frame`. This is assignment, not an equality check.

### Line 511

```python
        self.canvas.show_frame(frame)
```

Inside `begin_correction`: Run this operation: `self.canvas.show_frame`: copy a video frame, convert its colours, and fit it inside the canvas. Arguments: `frame`.

### Line 512

```python
        self.canvas.points = []
```

Inside `begin_correction`: Store the result in `self.canvas.points`: an empty list `[]`. This is assignment, not an equality check.

### Line 513

```python
        self.canvas.correcting = True
```

Inside `begin_correction`: Store the result in `self.canvas.correcting`: `True`. This is assignment, not an equality check.

### Line 514

```python
        self.canvas.click_limit = 2 if self.correction_mode == 'scale' else 3
```

Inside `begin_correction`: Store the result in `self.canvas.click_limit`: `2` when `self.correction_mode` equals `'scale'`; otherwise `3`. This is assignment, not an equality check.

### Line 515

```python
        if self.correction_mode == 'scale':
```

Inside `begin_correction`: Run the indented block only when this condition is true: `self.correction_mode` equals `'scale'`. Other branches handle the remaining case.

### Line 516

```python
            self.status.setText('Click the top then bottom of the known vertical reference. Use the same depth as the athlete.')
```

Inside `begin_correction`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `'Click the top then bottom of the known vertical reference. Use the same depth as the athlete.'`.

### Line 517

```python
            return
```

Inside `begin_correction`: End this function now and send back no explicit value. A bare return sends None.

### Line 518

```python
        self.status.setText('Click lip A, lip B, then the centre of the hip. Lip points must bracket the hip.')
```

Inside `begin_correction`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `'Click lip A, lip B, then the centre of the hip. Lip points must bracket the hip.'`.

### Line 519

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 520

```python
    def correct_points(self, points):
```

Inside `MainWindow`: Define `correct_points(self, points)`. Its job: draw clicked points, validate geometry, and save a corrected or manual candidate The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 521

```python
        if self.pending_manual is None and self.selected_jump() is not self.correction_jump:
```

Inside `correct_points`: Run the indented block only when this condition is true: `self.pending_manual` is the same object as `None` AND `self.selected_jump`: look up the candidate belonging to the selected table row. No arguments are supplied is not the same object as `self.correction_jump`. Other branches handle the remaining case.

### Line 522

```python
            self.canvas.correcting = False
```

Inside `correct_points`: Store the result in `self.canvas.correcting`: `False`. This is assignment, not an equality check.

### Line 523

```python
            return
```

Inside `correct_points`: End this function now and send back no explicit value. A bare return sends None.

### Line 524

```python
        marked = self.raw_frame.copy()
```

Inside `correct_points`: Store the result in `marked`: `self.raw_frame.copy`: make a separate copy so later drawing or changes do not overwrite the original. No arguments are supplied. This is assignment, not an equality check.

### Line 525

```python
        for point in points:
```

Inside `correct_points`: Repeat the following indented block for each `point` from `points`. Tuple targets unpack each loop item.

### Line 526

```python
            cv2.circle(marked, tuple(map(round, point)), 6, (80, 225, 255), -1)
```

Inside `correct_points`: Run this operation: `cv2.circle`: draw a point marker on the supplied image. Arguments: `marked`; `tuple`: create a tuple from the supplied values. Arguments: `map`: apply the first function to each supplied value. Arguments: `round`; `point`; `6`; tuple containing `80`; `225`; `255`; negative `1`.

### Line 527

```python
        self.canvas.show_frame(marked)
```

Inside `correct_points`: Run this operation: `self.canvas.show_frame`: copy a video frame, convert its colours, and fit it inside the canvas. Arguments: `marked`.

### Line 528

```python
        if self.correction_mode == 'scale':
```

Inside `correct_points`: Run the indented block only when this condition is true: `self.correction_mode` equals `'scale'`. Other branches handle the remaining case.

### Line 529

```python
            if len(points) == 2:
```

Inside `correct_points`: Run the indented block only when this condition is true: `len`: count items. Arguments: `points` equals `2`. Other branches handle the remaining case.

### Line 530

```python
                self.save_calibration(points)
```

Inside `correct_points`: Run this operation: `self.save_calibration`: validate a known vertical reference and save a metre estimate for this selected peak. Arguments: `points`.

### Line 531

```python
            return
```

Inside `correct_points`: End this function now and send back no explicit value. A bare return sends None.

### Line 532

```python
        if len(points) != 3:
```

Inside `correct_points`: Run the indented block only when this condition is true: `len`: count items. Arguments: `points` does not equal `3`. Other branches handle the remaining case.

### Line 533

```python
            self.status.setText(f"{len(points)} of 3 points set. Next: {['lip A', 'lip B', 'hip'][len(points)]}.")
```

Inside `correct_points`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: formatted text `f"{len(points)} of 3 points set. Next: {['lip A', 'lip B', 'hip'][len(points)]}."`. Inserted values: len(points); ['lip A', 'lip B', 'hip'][len(points)].

### Line 534

```python
            return
```

Inside `correct_points`: End this function now and send back no explicit value. A bare return sends None.

### Line 535

```python
        try:
```

Inside `correct_points`: Begin an operation with explicit error handling. The following except clauses handle failures; finally performs cleanup even after a return or error.

### Line 536

```python
            gap, metres, lip_y = measure_height(*points)
```

Inside `correct_points`: Store the result in `(gap, metres, lip_y)`: `measure_height`: interpolate the lip at the hip X coordinate and calculate a signed pixel gap. Arguments: `*points`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 537

```python
        except ValueError as error:
```

Inside `correct_points`: Handle the exception type(s) named here. `as error` stores the exception so a readable message can be shown or saved.

### Line 538

```python
            self.status.setText(str(error) + ' Click Correct to try again.')
```

Inside `correct_points`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: (`str`: convert a value to text. Arguments: `error` plus `' Click Correct to try again.'`).

### Line 539

```python
            self.canvas.correcting = False
```

Inside `correct_points`: Store the result in `self.canvas.correcting`: `False`. This is assignment, not an equality check.

### Line 540

```python
            return
```

Inside `correct_points`: End this function now and send back no explicit value. A bare return sends None.

### Line 541

```python
        if self.pending_manual is not None:
```

Inside `correct_points`: Run the indented block only when this condition is true: `self.pending_manual` is not the same object as `None`. Other branches handle the remaining case.

### Line 542

```python
            sample = dict(**self.pending_manual, person=dict(hip=list(points[2]), box=[points[2][0] - 20, points[2][1] - 30, 40, 60], points=[[0, 0, 0] for _ in range(17)], score=1.0, hip_score=1.0), lip=None, height_px=None, confidence=1.0, status='Manual measurement', cut=False, manual=True)
```

Inside `correct_points`: Store the result in `sample`: `dict`: create a dictionary from the named fields. Arguments: ** = `self.pending_manual`; person = `dict`: create a dictionary from the named fields. Arguments: hip = `list`: create a list from the supplied values. Arguments: `points[2]`; box = list containing (`points[2][0]` minus `20`); (`points[2][1]` minus `30`); `40`; `60`; points = produce list containing `0`; `0`; `0`, for each _ in `range`: produce integer loop positions, excluding the upper bound. Arguments: `17`; score = `1.0`; hip_score = `1.0`; lip = `None`; height_px = `None`; confidence = `1.0`; status = `'Manual measurement'`; cut = `False`; manual = `True`. This is assignment, not an equality check.

### Line 543

```python
            jump = dict(id=max((item['id'] for item in self.report['jumps']), default=0) + 1, start=sample['time'], end=sample['time'], peak_time=sample['time'], frame=sample['frame'], height_px=gap, height_m=None, scale=None, confidence=1.0, reviewed=True, excluded=False, reasons=[], sample_index=len(self.report['samples']), manual=True)
```

Inside `correct_points`: Store the result in `jump`: `dict`: create a dictionary from the named fields. Arguments: id = (`max`: choose the largest value, or the item with the largest key. Arguments: produce `item['id']`, for each item in `self.report['jumps']`; default = `0` plus `1`); start = `sample['time']`; end = `sample['time']`; peak_time = `sample['time']`; frame = `sample['frame']`; height_px = `gap`; height_m = `None`; scale = `None`; confidence = `1.0`; reviewed = `True`; excluded = `False`; reasons = an empty list `[]`; sample_index = `len`: count items. Arguments: `self.report['samples']`; manual = `True`. This is assignment, not an equality check.

### Line 544

```python
            self.report['samples'].append(sample)
```

Inside `correct_points`: Run this operation: `self.report['samples'].append`: add an item to the end of this list. Arguments: `sample`.

### Line 545

```python
            self.report['jumps'].append(jump)
```

Inside `correct_points`: Run this operation: `self.report['jumps'].append`: add an item to the end of this list. Arguments: `jump`.

### Line 546

```python
            self.refresh_results()
```

Inside `correct_points`: Run this operation: `self.refresh_results`: rebuild table rows and update the candidate count, coverage, and timeline. No arguments are supplied.

### Line 547

```python
            self.table.selectRow(len(self.report['jumps']) - 1)
```

Inside `correct_points`: Run this operation: `self.table.selectRow`: select the requested result row. Arguments: (`len`: count items. Arguments: `self.report['jumps']` minus `1`).

### Line 548

```python
            self.pending_manual = None
```

Inside `correct_points`: Store the result in `self.pending_manual`: `None`. This is assignment, not an equality check.

### Line 549

```python
        else:
```

Inside `correct_points`: Run this branch when the preceding condition was false.

### Line 550

```python
            jump = self.correction_jump
```

Inside `correct_points`: Store the result in `jump`: `self.correction_jump`. This is assignment, not an equality check.

### Line 551

```python
        sample = self.report['samples'][jump['sample_index']]
```

Inside `correct_points`: Store the result in `sample`: `self.report['samples'][jump['sample_index']]`. This is assignment, not an equality check.

### Line 552

```python
        sample['person']['hip'] = list(points[2])
```

Inside `correct_points`: Store the result in `sample['person']['hip']`: `list`: create a list from the supplied values. Arguments: `points[2]`. This is assignment, not an equality check.

### Line 553

```python
        sample['lip'] = dict(a=list(points[0]), b=list(points[1]), y=lip_y, score=1.0, extrapolated=False)
```

Inside `correct_points`: Store the result in `sample['lip']`: `dict`: create a dictionary from the named fields. Arguments: a = `list`: create a list from the supplied values. Arguments: `points[0]`; b = `list`: create a list from the supplied values. Arguments: `points[1]`; y = `lip_y`; score = `1.0`; extrapolated = `False`. This is assignment, not an equality check.

### Line 554

```python
        sample['height_px'] = gap
```

Inside `correct_points`: Store the result in `sample['height_px']`: `gap`. This is assignment, not an equality check.

### Line 555

```python
        jump.update(height_px=round(gap, 2), height_m=None, scale=None, calibration=None, reviewed=True, corrected=True, reasons=['Points corrected manually. Camera scale is still uncalibrated.'])
```

Inside `correct_points`: Run this operation: `jump.update`: replace or add the supplied named fields. Arguments: height_px = `round`: round a number to the requested precision. Arguments: `gap`; `2`; height_m = `None`; scale = `None`; calibration = `None`; reviewed = `True`; corrected = `True`; reasons = list containing `'Points corrected manually. Camera scale is still uncalibrated.'`.

### Line 556

```python
        self.canvas.correcting = False
```

Inside `correct_points`: Store the result in `self.canvas.correcting`: `False`. This is assignment, not an equality check.

### Line 557

```python
        jump['snapshot'] = f"jump-{jump['id']:03}-corrected.jpg"
```

Inside `correct_points`: Store the result in `jump['snapshot']`: formatted text `f"jump-{jump['id']:03}-corrected.jpg"`. Inserted values: jump['id'], format f'03'. This is assignment, not an equality check.

### Line 558

```python
        cv2.imwrite(str(Path(self.report['folder']) / jump['snapshot']), annotate(self.raw_frame, sample))
```

Inside `correct_points`: Run this operation: `cv2.imwrite`: encode and save an image at the supplied path. Arguments: `str`: convert a value to text. Arguments: (`Path`: create a filesystem path object. Arguments: `self.report['folder']` divided by `jump['snapshot']`); `annotate`: copy an image and draw the box, body points, hip, lip, and measurement. Arguments: `self.raw_frame`; `sample`.

### Line 559

```python
        self.persist()
```

Inside `correct_points`: Run this operation: `self.persist`: save the changed report and CSV and restore the current table selection. No arguments are supplied.

### Line 560

```python
        self.canvas.show_frame(annotate(self.raw_frame, sample))
```

Inside `correct_points`: Run this operation: `self.canvas.show_frame`: copy a video frame, convert its colours, and fit it inside the canvas. Arguments: `annotate`: copy an image and draw the box, body points, hip, lip, and measurement. Arguments: `self.raw_frame`; `sample`.

### Line 561

```python
        self.status.setText('Corrected points saved. Apply a valid scale only if it is known for this peak.')
```

Inside `correct_points`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `'Corrected points saved. Apply a valid scale only if it is known for this peak.'`.

### Line 562

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 563

```python
    def start_calibration(self):
```

Inside `MainWindow`: Define `start_calibration(self)`. Its job: load the selected original peak frame for a two-point known vertical reference The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 564

```python
        jump = self.selected_jump()
```

Inside `start_calibration`: Store the result in `jump`: `self.selected_jump`: look up the candidate belonging to the selected table row. No arguments are supplied. This is assignment, not an equality check.

### Line 565

```python
        if not jump or (self.worker and self.worker.isRunning()) or (self.frame_worker and self.frame_worker.isRunning()):
```

Inside `start_calibration`: Run the indented block only when this condition is true: NOT `jump` OR `self.worker` AND `self.worker.isRunning`: check whether this worker thread is active. No arguments are supplied OR `self.frame_worker` AND `self.frame_worker.isRunning`: check whether this worker thread is active. No arguments are supplied. Other branches handle the remaining case.

### Line 566

```python
            return
```

Inside `start_calibration`: End this function now and send back no explicit value. A bare return sends None.

### Line 567

```python
        self.correction_mode = 'scale'
```

Inside `start_calibration`: Store the result in `self.correction_mode`: `'scale'`. This is assignment, not an equality check.

### Line 568

```python
        self.correction_jump = jump
```

Inside `start_calibration`: Store the result in `self.correction_jump`: `jump`. This is assignment, not an equality check.

### Line 569

```python
        self.pending_manual = None
```

Inside `start_calibration`: Store the result in `self.pending_manual`: `None`. This is assignment, not an equality check.

### Line 570

```python
        self.frame_worker = FrameWorker(self.report['source'], jump['frame'])
```

Inside `start_calibration`: Store the result in `self.frame_worker`: `FrameWorker`: call this function with the supplied arguments. Arguments: `self.report['source']`; `jump['frame']`. This is assignment, not an equality check.

### Line 571

```python
        self.frame_worker.loaded.connect(self.begin_correction)
```

Inside `start_calibration`: Run this operation: `self.frame_worker.loaded.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.begin_correction`.

### Line 572

```python
        self.frame_worker.failed.connect(self.show_error)
```

Inside `start_calibration`: Run this operation: `self.frame_worker.failed.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.show_error`.

### Line 573

```python
        self.frame_worker.finished.connect(self.correction_loaded)
```

Inside `start_calibration`: Run this operation: `self.frame_worker.finished.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.correction_loaded`.

### Line 574

```python
        self.correct_button.setEnabled(False)
```

Inside `start_calibration`: Run this operation: `self.correct_button.setEnabled`: enable or disable this control. Arguments: `False`.

### Line 575

```python
        self.table.setEnabled(False)
```

Inside `start_calibration`: Run this operation: `self.table.setEnabled`: enable or disable this control. Arguments: `False`.

### Line 576

```python
        self.status.setText('Loading the peak frame for a local metre reference...')
```

Inside `start_calibration`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `'Loading the peak frame for a local metre reference...'`.

### Line 577

```python
        self.frame_worker.start()
```

Inside `start_calibration`: Run this operation: `self.frame_worker.start`: start the worker thread; Qt then calls its run method. No arguments are supplied.

### Line 578

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 579

```python
    def save_calibration(self, points):
```

Inside `MainWindow`: Define `save_calibration(self, points)`. Its job: validate a known vertical reference and save a metre estimate for this selected peak The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 580

```python
        jump = self.correction_jump
```

Inside `save_calibration`: Store the result in `jump`: `self.correction_jump`. This is assignment, not an equality check.

### Line 581

```python
        sample = self.report['samples'][jump['sample_index']]
```

Inside `save_calibration`: Store the result in `sample`: `self.report['samples'][jump['sample_index']]`. This is assignment, not an equality check.

### Line 582

```python
        try:
```

Inside `save_calibration`: Begin an operation with explicit error handling. The following except clauses handle failures; finally performs cleanup even after a return or error.

### Line 583

```python
            metres, scale, projected_gap = calibrate_height(sample['lip']['a'], sample['lip']['b'], sample['person']['hip'], points[0], points[1], self.reference_length.value())
```

Inside `save_calibration`: Store the result in `(metres, scale, projected_gap)`: `calibrate_height`: intersect the local vertical through the hip with the lip, then convert its signed distance using a known reference length. Arguments: `sample['lip']['a']`; `sample['lip']['b']`; `sample['person']['hip']`; `points[0]`; `points[1]`; `self.reference_length.value`: read the current numeric input value. No arguments are supplied. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 584

```python
        except ValueError as error:
```

Inside `save_calibration`: Handle the exception type(s) named here. `as error` stores the exception so a readable message can be shown or saved.

### Line 585

```python
            self.canvas.correcting = False
```

Inside `save_calibration`: Store the result in `self.canvas.correcting`: `False`. This is assignment, not an equality check.

### Line 586

```python
            self.status.setText(str(error) + ' Click Calibrate to try again.')
```

Inside `save_calibration`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: (`str`: convert a value to text. Arguments: `error` plus `' Click Calibrate to try again.'`).

### Line 587

```python
            return
```

Inside `save_calibration`: End this function now and send back no explicit value. A bare return sends None.

### Line 588

```python
        jump.update(height_m=round(metres, 3), scale=scale, calibration=dict(top=points[0], bottom=points[1], reference_metres=self.reference_length.value(), projected_gap_px=projected_gap, method='local_vertical_reference'))
```

Inside `save_calibration`: Run this operation: `jump.update`: replace or add the supplied named fields. Arguments: height_m = `round`: round a number to the requested precision. Arguments: `metres`; `3`; scale = `scale`; calibration = `dict`: create a dictionary from the named fields. Arguments: top = `points[0]`; bottom = `points[1]`; reference_metres = `self.reference_length.value`: read the current numeric input value. No arguments are supplied; projected_gap_px = `projected_gap`; method = `'local_vertical_reference'`.

### Line 589

```python
        jump['reasons'] = [reason for reason in jump['reasons'] if not reason.startswith('Camera scale')]
```

Inside `save_calibration`: Store the result in `jump['reasons']`: produce `reason`, for each reason in `jump['reasons']`, keeping only NOT `reason.startswith`: call this function with the supplied arguments. Arguments: `'Camera scale'`. This is assignment, not an equality check.

### Line 590

```python
        jump['reasons'].append('Local metre estimate. Reference depth and camera geometry need validation.')
```

Inside `save_calibration`: Run this operation: `jump['reasons'].append`: add an item to the end of this list. Arguments: `'Local metre estimate. Reference depth and camera geometry need validation.'`.

### Line 591

```python
        self.canvas.correcting = False
```

Inside `save_calibration`: Store the result in `self.canvas.correcting`: `False`. This is assignment, not an equality check.

### Line 592

```python
        self.persist()
```

Inside `save_calibration`: Run this operation: `self.persist`: save the changed report and CSV and restore the current table selection. No arguments are supplied.

### Line 593

```python
        self.status.setText('Metre estimate saved for this jump. A changed camera or depth needs a new reference.')
```

Inside `save_calibration`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `'Metre estimate saved for this jump. A changed camera or depth needs a new reference.'`.

### Line 594

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 595

```python
    def mark_reviewed(self):
```

Inside `MainWindow`: Define `mark_reviewed(self)`. Its job: mark the selected candidate reviewed and restore it if previously excluded The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 596

```python
        jump = self.selected_jump()
```

Inside `mark_reviewed`: Store the result in `jump`: `self.selected_jump`: look up the candidate belonging to the selected table row. No arguments are supplied. This is assignment, not an equality check.

### Line 597

```python
        if jump:
```

Inside `mark_reviewed`: Run the indented block only when this condition is true: `jump`. Other branches handle the remaining case.

### Line 598

```python
            jump.update(reviewed=True, excluded=False)
```

Inside `mark_reviewed`: Run this operation: `jump.update`: replace or add the supplied named fields. Arguments: reviewed = `True`; excluded = `False`.

### Line 599

```python
            self.persist()
```

Inside `mark_reviewed`: Run this operation: `self.persist`: save the changed report and CSV and restore the current table selection. No arguments are supplied.

### Line 600

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 601

```python
    def exclude(self):
```

Inside `MainWindow`: Define `exclude(self)`. Its job: mark a candidate excluded while retaining its row and evidence The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 602

```python
        jump = self.selected_jump()
```

Inside `exclude`: Store the result in `jump`: `self.selected_jump`: look up the candidate belonging to the selected table row. No arguments are supplied. This is assignment, not an equality check.

### Line 603

```python
        if jump:
```

Inside `exclude`: Run the indented block only when this condition is true: `jump`. Other branches handle the remaining case.

### Line 604

```python
            jump.update(excluded=True, reviewed=True)
```

Inside `exclude`: Run this operation: `jump.update`: replace or add the supplied named fields. Arguments: excluded = `True`; reviewed = `True`.

### Line 605

```python
            self.persist()
```

Inside `exclude`: Run this operation: `self.persist`: save the changed report and CSV and restore the current table selection. No arguments are supplied.

### Line 606

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 607

```python
    def persist(self):
```

Inside `MainWindow`: Define `persist(self)`. Its job: save the changed report and CSV and restore the current table selection The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 608

```python
        row = self.table.currentRow()
```

Inside `persist`: Store the result in `row`: `self.table.currentRow`: read the selected row index, or -1 if no row is selected. No arguments are supplied. This is assignment, not an equality check.

### Line 609

```python
        try:
```

Inside `persist`: Begin an operation with explicit error handling. The following except clauses handle failures; finally performs cleanup even after a return or error.

### Line 610

```python
            save_report(self.report, self.report['folder'])
```

Inside `persist`: Run this operation: `save_report`: write the complete JSON session through a temporary file. Arguments: `self.report`; `self.report['folder']`.

### Line 611

```python
            export_csv(self.report, Path(self.report['folder']) / 'jumps.csv')
```

Inside `persist`: Run this operation: `export_csv`: write candidate rows including their review and exclusion flags. Arguments: `self.report`; (`Path`: create a filesystem path object. Arguments: `self.report['folder']` divided by `'jumps.csv'`).

### Line 612

```python
        except OSError as error:
```

Inside `persist`: Handle the exception type(s) named here. `as error` stores the exception so a readable message can be shown or saved.

### Line 613

```python
            self.show_error(str(error))
```

Inside `persist`: Run this operation: `self.show_error`: show a readable status and warning dialog. Arguments: `str`: convert a value to text. Arguments: `error`.

### Line 614

```python
            return
```

Inside `persist`: End this function now and send back no explicit value. A bare return sends None.

### Line 615

```python
        self.refresh_results()
```

Inside `persist`: Run this operation: `self.refresh_results`: rebuild table rows and update the candidate count, coverage, and timeline. No arguments are supplied.

### Line 616

```python
        if row >= 0:
```

Inside `persist`: Run the indented block only when this condition is true: `row` is at least `0`. Other branches handle the remaining case.

### Line 617

```python
            self.table.selectRow(row)
```

Inside `persist`: Run this operation: `self.table.selectRow`: select the requested result row. Arguments: `row`.

### Line 618

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 619

```python
    def export_results(self):
```

Inside `MainWindow`: Define `export_results(self)`. Its job: ask for an export path and write the candidate table The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 620

```python
        if not self.report:
```

Inside `export_results`: Run the indented block only when this condition is true: NOT `self.report`. Other branches handle the remaining case.

### Line 621

```python
            self.status.setText('Analyse a video or open a saved session first.')
```

Inside `export_results`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `'Analyse a video or open a saved session first.'`.

### Line 622

```python
            return
```

Inside `export_results`: End this function now and send back no explicit value. A bare return sends None.

### Line 623

```python
        path, kind = QFileDialog.getSaveFileName(self, 'Export jump results', 'jumps.csv', 'CSV (*.csv)')
```

Inside `export_results`: Store the result in `(path, kind)`: `QFileDialog.getSaveFileName`: ask the user for an export destination. Arguments: `self`; `'Export jump results'`; `'jumps.csv'`; `'CSV (*.csv)'`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 624

```python
        if path:
```

Inside `export_results`: Run the indented block only when this condition is true: `path`. Other branches handle the remaining case.

### Line 625

```python
            try:
```

Inside `export_results`: Begin an operation with explicit error handling. The following except clauses handle failures; finally performs cleanup even after a return or error.

### Line 626

```python
                export_csv(self.report, path)
```

Inside `export_results`: Run this operation: `export_csv`: write candidate rows including their review and exclusion flags. Arguments: `self.report`; `path`.

### Line 627

```python
                self.status.setText(f'Exported {Path(path).name}. Review and exclusion columns are included.')
```

Inside `export_results`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: formatted text `f'Exported {Path(path).name}. Review and exclusion columns are included.'`. Inserted values: Path(path).name.

### Line 628

```python
            except OSError as error:
```

Inside `export_results`: Handle the exception type(s) named here. `as error` stores the exception so a readable message can be shown or saved.

### Line 629

```python
                self.show_error(str(error))
```

Inside `export_results`: Run this operation: `self.show_error`: show a readable status and warning dialog. Arguments: `str`: convert a value to text. Arguments: `error`.

### Line 630

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 631

```python
    def open_session(self):
```

Inside `MainWindow`: Define `open_session(self)`. Its job: ask for a saved report when no background task is active The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 632

```python
        if (self.worker and self.worker.isRunning()) or (self.frame_worker and self.frame_worker.isRunning()):
```

Inside `open_session`: Run the indented block only when this condition is true: `self.worker` AND `self.worker.isRunning`: check whether this worker thread is active. No arguments are supplied OR `self.frame_worker` AND `self.frame_worker.isRunning`: check whether this worker thread is active. No arguments are supplied. Other branches handle the remaining case.

### Line 633

```python
            self.status.setText('Stop the current task before opening another session.')
```

Inside `open_session`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `'Stop the current task before opening another session.'`.

### Line 634

```python
            return
```

Inside `open_session`: End this function now and send back no explicit value. A bare return sends None.

### Line 635

```python
        path, kind = QFileDialog.getOpenFileName(self, 'Open report.json', str(data_folder() / 'sessions'), 'Session (*.json)')
```

Inside `open_session`: Store the result in `(path, kind)`: `QFileDialog.getOpenFileName`: ask the user to select a file, returning its path and filter. Arguments: `self`; `'Open report.json'`; `str`: convert a value to text. Arguments: (`data_folder`: get a writable folder for this user's models and sessions. No arguments are supplied divided by `'sessions'`); `'Session (*.json)'`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 636

```python
        if path:
```

Inside `open_session`: Run the indented block only when this condition is true: `path`. Other branches handle the remaining case.

### Line 637

```python
            self.read_session(path)
```

Inside `open_session`: Run this operation: `self.read_session`: read and validate the supported session format and display it. Arguments: `path`.

### Line 638

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 639

```python
    def read_session(self, path):
```

Inside `MainWindow`: Define `read_session(self, path)`. Its job: read and validate the supported session format and display it The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 640

```python
        try:
```

Inside `read_session`: Begin an operation with explicit error handling. The following except clauses handle failures; finally performs cleanup even after a return or error.

### Line 641

```python
            report = json.loads(Path(path).read_text(encoding='utf-8'))
```

Inside `read_session`: Store the result in `report`: `json.loads`: parse JSON text back into Python values. Arguments: `Path(path).read_text`: read a complete text file with the selected encoding. Arguments: encoding = `'utf-8'`. This is assignment, not an equality check.

### Line 642

```python
            if report.get('version') != 2 or not isinstance(report.get('samples'), list) or not isinstance(report.get('jumps'), list):
```

Inside `read_session`: Run the indented block only when this condition is true: `report.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'version'` does not equal `2` OR NOT `isinstance`: call this function with the supplied arguments. Arguments: `report.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'samples'`; `list` OR NOT `isinstance`: call this function with the supplied arguments. Arguments: `report.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `'jumps'`; `list`. Other branches handle the remaining case.

### Line 643

```python
                raise ValueError('This is not a supported Lip session.')
```

Inside `read_session`: Stop this operation by raising an exception: `ValueError`: call this function with the supplied arguments. Arguments: `'This is not a supported Lip session.'`. A matching except block can handle it.

### Line 644

```python
            report['folder'] = str(Path(path).parent)
```

Inside `read_session`: Store the result in `report['folder']`: `str`: convert a value to text. Arguments: `Path(path).parent`. This is assignment, not an equality check.

### Line 645

```python
            self.receive_report(report)
```

Inside `read_session`: Run this operation: `self.receive_report`: replace the displayed session and refresh its candidates and metrics. Arguments: `report`.

### Line 646

```python
        except (OSError, ValueError, KeyError) as error:
```

Inside `read_session`: Handle the exception type(s) named here. `as error` stores the exception so a readable message can be shown or saved.

### Line 647

```python
            self.show_error(str(error))
```

Inside `read_session`: Run this operation: `self.show_error`: show a readable status and warning dialog. Arguments: `str`: convert a value to text. Arguments: `error`.

### Line 648

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 649

```python
    def open_results(self):
```

Inside `MainWindow`: Define `open_results(self)`. Its job: open this session's folder in the normal Windows file browser The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 650

```python
        folder = Path(self.report['folder']) if self.report else data_folder() / 'sessions'
```

Inside `open_results`: Store the result in `folder`: `Path`: create a filesystem path object. Arguments: `self.report['folder']` when `self.report`; otherwise (`data_folder`: get a writable folder for this user's models and sessions. No arguments are supplied divided by `'sessions'`). This is assignment, not an equality check.

### Line 651

```python
        folder.mkdir(parents=True, exist_ok=True)
```

Inside `open_results`: Run this operation: `folder.mkdir`: create the folder, optionally creating parents and accepting an existing folder. Arguments: parents = `True`; exist_ok = `True`.

### Line 652

```python
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))
```

Inside `open_results`: Run this operation: `QDesktopServices.openUrl`: ask Windows to open a local folder, file, or URL with its registered app. Arguments: `QUrl.fromLocalFile`: create a correctly escaped local-file URL. Arguments: `str`: convert a value to text. Arguments: `folder`.

### Line 653

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 654

```python
    def open_review_video(self):
```

Inside `MainWindow`: Define `open_review_video(self)`. Its job: open the sampled marked playback in the default video player The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 655

```python
        if self.report and (Path(self.report['folder']) / 'review.mp4').exists():
```

Inside `open_review_video`: Run the indented block only when this condition is true: `self.report` AND `(Path(self.report['folder']) / 'review.mp4').exists`: check whether this path currently exists. No arguments are supplied. Other branches handle the remaining case.

### Line 656

```python
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(Path(self.report['folder']) / 'review.mp4')))
```

Inside `open_review_video`: Run this operation: `QDesktopServices.openUrl`: ask Windows to open a local folder, file, or URL with its registered app. Arguments: `QUrl.fromLocalFile`: create a correctly escaped local-file URL. Arguments: `str`: convert a value to text. Arguments: (`Path`: create a filesystem path object. Arguments: `self.report['folder']` divided by `'review.mp4'`).

### Line 657

```python
        else:
```

Inside `open_review_video`: Run this branch when the preceding condition was false.

### Line 658

```python
            self.status.setText('No marked review video is available for this session yet.')
```

Inside `open_review_video`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `'No marked review video is available for this session yet.'`.

### Line 659

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 660

```python
    def save_recent(self):
```

Inside `MainWindow`: Define `save_recent(self)`. Its job: save a small pointer to the last opened report The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 661

```python
        if self.report:
```

Inside `save_recent`: Run the indented block only when this condition is true: `self.report`. Other branches handle the remaining case.

### Line 662

```python
            (data_folder() / 'recent.json').write_text(json.dumps(dict(report=str(Path(self.report['folder']) / 'report.json'))), encoding='utf-8')
```

Inside `save_recent`: Run this operation: `(data_folder() / 'recent.json').write_text`: write text to a file with the selected encoding. Arguments: `json.dumps`: serialize dictionaries and lists to JSON text. Arguments: `dict`: create a dictionary from the named fields. Arguments: report = `str`: convert a value to text. Arguments: (`Path`: create a filesystem path object. Arguments: `self.report['folder']` divided by `'report.json'`); encoding = `'utf-8'`.

### Line 663

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 664

```python
    def load_recent(self):
```

Inside `MainWindow`: Define `load_recent(self)`. Its job: try to reopen the last report without interrupting startup if it is absent The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 665

```python
        try:
```

Inside `load_recent`: Begin an operation with explicit error handling. The following except clauses handle failures; finally performs cleanup even after a return or error.

### Line 666

```python
            recent = json.loads((data_folder() / 'recent.json').read_text(encoding='utf-8'))
```

Inside `load_recent`: Store the result in `recent`: `json.loads`: parse JSON text back into Python values. Arguments: `(data_folder() / 'recent.json').read_text`: read a complete text file with the selected encoding. Arguments: encoding = `'utf-8'`. This is assignment, not an equality check.

### Line 667

```python
            if Path(recent['report']).exists():
```

Inside `load_recent`: Run the indented block only when this condition is true: `Path(recent['report']).exists`: check whether this path currently exists. No arguments are supplied. Other branches handle the remaining case.

### Line 668

```python
                self.read_session(recent['report'])
```

Inside `load_recent`: Run this operation: `self.read_session`: read and validate the supported session format and display it. Arguments: `recent['report']`.

### Line 669

```python
        except (OSError, ValueError, KeyError):
```

Inside `load_recent`: Handle the exception type(s) named here. `as error` stores the exception so a readable message can be shown or saved.

### Line 670

```python
            pass
```

Inside `load_recent`: Do nothing in this branch. Here the missing or unreadable optional recent-session pointer is deliberately ignored.

### Line 671

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 672

```python
    def show_error(self, message):
```

Inside `MainWindow`: Define `show_error(self, message)`. Its job: show a readable status and warning dialog The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 673

```python
        self.status.setText(message)
```

Inside `show_error`: Run this operation: `self.status.setText`: replace the visible label or input text. Arguments: `message`.

### Line 674

```python
        QMessageBox.warning(self, 'Lip', message)
```

Inside `show_error`: Run this operation: `QMessageBox.warning`: show a warning dialog with the supplied title and message. Arguments: `self`; `'Lip'`; `message`.

### Line 675

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 676

```python
    def dragEnterEvent(self, event):
```

Inside `MainWindow`: Define `dragEnterEvent(self, event)`. Its job: accept a dragged file or link that can supply a video source The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 677

```python
        if event.mimeData().hasUrls():
```

Inside `dragEnterEvent`: Run the indented block only when this condition is true: `event.mimeData().hasUrls`: check whether the drag contains files or links. No arguments are supplied. Other branches handle the remaining case.

### Line 678

```python
            event.acceptProposedAction()
```

Inside `dragEnterEvent`: Run this operation: `event.acceptProposedAction`: accept the drag or drop action supplied by Windows. No arguments are supplied.

### Line 679

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 680

```python
    def dropEvent(self, event):
```

Inside `MainWindow`: Define `dropEvent(self, event)`. Its job: put a dropped file path or link into the source input The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 681

```python
        url = event.mimeData().urls()[0]
```

Inside `dropEvent`: Store the result in `url`: `event.mimeData().urls()[0]`. This is assignment, not an equality check.

### Line 682

```python
        self.source.setText(url.toLocalFile() if url.isLocalFile() else url.toString())
```

Inside `dropEvent`: Run this operation: `self.source.setText`: replace the visible label or input text. Arguments: `url.toLocalFile`: convert the URL to a Windows path. No arguments are supplied when `url.isLocalFile`: check whether the URL refers to a local file. No arguments are supplied; otherwise `url.toString`: convert the URL to link text. No arguments are supplied.

### Line 683

```python

```

Inside `MainWindow`: Blank line. It separates related parts for readability and performs no operation.

### Line 684

```python
    def closeEvent(self, event):
```

Inside `MainWindow`: Define `closeEvent(self, event)`. Its job: stop running work safely before allowing the window to close The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 685

```python
        running = (self.worker and self.worker.isRunning()) or (self.frame_worker and self.frame_worker.isRunning())
```

Inside `closeEvent`: Store the result in `running`: `self.worker` AND `self.worker.isRunning`: check whether this worker thread is active. No arguments are supplied OR `self.frame_worker` AND `self.frame_worker.isRunning`: check whether this worker thread is active. No arguments are supplied. This is assignment, not an equality check.

### Line 686

```python
        if running:
```

Inside `closeEvent`: Run the indented block only when this condition is true: `running`. Other branches handle the remaining case.

### Line 687

```python
            self.close_pending = True
```

Inside `closeEvent`: Store the result in `self.close_pending`: `True`. This is assignment, not an equality check.

### Line 688

```python
            self.stop_analysis()
```

Inside `closeEvent`: Run this operation: `self.stop_analysis`: request an orderly stop and keep the partial session. No arguments are supplied.

### Line 689

```python
            if self.frame_worker and self.frame_worker.isRunning():
```

Inside `closeEvent`: Run the indented block only when this condition is true: `self.frame_worker` AND `self.frame_worker.isRunning`: check whether this worker thread is active. No arguments are supplied. Other branches handle the remaining case.

### Line 690

```python
                self.frame_worker.finished.connect(self.close)
```

Inside `closeEvent`: Run this operation: `self.frame_worker.finished.connect`: register the function to run when this Qt signal is emitted. Arguments: `self.close`.

### Line 691

```python
            event.ignore()
```

Inside `closeEvent`: Run this operation: `event.ignore`: delay the close event while active work is cleaned up. No arguments are supplied.

### Line 692

```python
        else:
```

Inside `closeEvent`: Run this branch when the preceding condition was false.

### Line 693

```python
            event.accept()
```

Inside `closeEvent`: Run this operation: `event.accept`: allow the close event to complete. No arguments are supplied.

### Line 694

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 695

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 696

```python
if __name__ == '__main__':
```

Run the indented block only when this condition is true: `__name__` equals `'__main__'`. Other branches handle the remaining case.

### Line 697

```python
    application = QApplication(sys.argv)
```

Store the result in `application`: `QApplication`: create the Qt application and event loop owner. Arguments: `sys.argv`. This is assignment, not an equality check.

### Line 698

```python
    application.setStyle('Fusion')
```

Run this operation: `application.setStyle`: choose Qt's control appearance style. Arguments: `'Fusion'`.

### Line 699

```python
    application.setStyleSheet(STYLE)
```

Run this operation: `application.setStyleSheet`: apply the supplied Qt styling rules. Arguments: `STYLE`.

### Line 700

```python
    window = MainWindow()
```

Store the result in `window`: `MainWindow`: call this function with the supplied arguments. No arguments are supplied. This is assignment, not an equality check.

### Line 701

```python
    if len(sys.argv) > 1:
```

Run the indented block only when this condition is true: `len`: count items. Arguments: `sys.argv` is greater than `1`. Other branches handle the remaining case.

### Line 702

```python
        if sys.argv[1].endswith('.json'):
```

Run the indented block only when this condition is true: `sys.argv[1].endswith`: call this function with the supplied arguments. Arguments: `'.json'`. Other branches handle the remaining case.

### Line 703

```python
            window.read_session(sys.argv[1])
```

Run this operation: `window.read_session`: read and validate the supported session format and display it. Arguments: `sys.argv[1]`.

### Line 704

```python
        else:
```

Run this branch when the preceding condition was false.

### Line 705

```python
            window.source.setText(sys.argv[1])
```

Run this operation: `window.source.setText`: replace the visible label or input text. Arguments: `sys.argv[1]`.

### Line 706

```python
    window.show()
```

Run this operation: `window.show`: make the window visible. No arguments are supplied.

### Line 707

```python
    sys.exit(application.exec())
```

Run this operation: `sys.exit`: return the application's exit code to the operating system. Arguments: `application.exec`: run Qt's event loop until the application exits. No arguments are supplied.

## test_measurement.py

Source SHA-256: `b0e04a85d7ba9a488a7ba5da5ecdff78197f44c7b815988534a65249801899e2`

### Line 1

```python
"""Small checks for the measurement formula and invalid inputs."""
```

Documentation string: Small checks for the measurement formula and invalid inputs. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 2

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 3

```python
import unittest
```

Import modules: unittest. Their functions become available through those module names.

### Line 4

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 5

```python
from measurement import measure_height
```

Import measure_height from `measurement`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 6

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 7

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 8

```python
class MeasurementTests(unittest.TestCase):
```

Define the `MeasurementTests` class, inheriting from unittest.TestCase. Check cases that could otherwise produce a misleading measurement.

### Line 9

```python
    """Check cases that could otherwise produce a misleading measurement."""
```

Inside `MeasurementTests`: Documentation string: Check cases that could otherwise produce a misleading measurement. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 10

```python

```

Inside `MeasurementTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 11

```python
    def test_horizontal_lip(self):
```

Inside `MeasurementTests`: Define `test_horizontal_lip(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 12

```python
        result = measure_height((100, 400), (800, 400), (450, 160), 80)
```

Inside `test_horizontal_lip`: Store the result in `result`: `measure_height`: interpolate the lip at the hip X coordinate and calculate a signed pixel gap. Arguments: tuple containing `100`; `400`; tuple containing `800`; `400`; tuple containing `450`; `160`; `80`. This is assignment, not an equality check.

### Line 13

```python
        self.assertEqual(result, (240, 3, 400))
```

Inside `test_horizontal_lip`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `result`; tuple containing `240`; `3`; `400`.

### Line 14

```python

```

Inside `MeasurementTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 15

```python
    def test_sloped_lip(self):
```

Inside `MeasurementTests`: Define `test_sloped_lip(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 16

```python
        result = measure_height((100, 300), (500, 500), (300, 250))
```

Inside `test_sloped_lip`: Store the result in `result`: `measure_height`: interpolate the lip at the hip X coordinate and calculate a signed pixel gap. Arguments: tuple containing `100`; `300`; tuple containing `500`; `500`; tuple containing `300`; `250`. This is assignment, not an equality check.

### Line 17

```python
        self.assertEqual(result, (150, None, 400))
```

Inside `test_sloped_lip`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `result`; tuple containing `150`; `None`; `400`.

### Line 18

```python

```

Inside `MeasurementTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 19

```python
    def test_reversed_lip_points(self):
```

Inside `MeasurementTests`: Define `test_reversed_lip_points(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 20

```python
        result = measure_height((500, 500), (100, 300), (300, 250))
```

Inside `test_reversed_lip_points`: Store the result in `result`: `measure_height`: interpolate the lip at the hip X coordinate and calculate a signed pixel gap. Arguments: tuple containing `500`; `500`; tuple containing `100`; `300`; tuple containing `300`; `250`. This is assignment, not an equality check.

### Line 21

```python
        self.assertEqual(result, (150, None, 400))
```

Inside `test_reversed_lip_points`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `result`; tuple containing `150`; `None`; `400`.

### Line 22

```python

```

Inside `MeasurementTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 23

```python
    def test_below_lip_is_negative(self):
```

Inside `MeasurementTests`: Define `test_below_lip_is_negative(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 24

```python
        result = measure_height((100, 400), (800, 400), (450, 450))
```

Inside `test_below_lip_is_negative`: Store the result in `result`: `measure_height`: interpolate the lip at the hip X coordinate and calculate a signed pixel gap. Arguments: tuple containing `100`; `400`; tuple containing `800`; `400`; tuple containing `450`; `450`. This is assignment, not an equality check.

### Line 25

```python
        self.assertEqual(result[0], -50)
```

Inside `test_below_lip_is_negative`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `result[0]`; negative `50`.

### Line 26

```python

```

Inside `MeasurementTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 27

```python
    def test_on_lip_is_zero(self):
```

Inside `MeasurementTests`: Define `test_on_lip_is_zero(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 28

```python
        result = measure_height((100, 400), (800, 400), (450, 400))
```

Inside `test_on_lip_is_zero`: Store the result in `result`: `measure_height`: interpolate the lip at the hip X coordinate and calculate a signed pixel gap. Arguments: tuple containing `100`; `400`; tuple containing `800`; `400`; tuple containing `450`; `400`. This is assignment, not an equality check.

### Line 29

```python
        self.assertEqual(result[0], 0)
```

Inside `test_on_lip_is_zero`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `result[0]`; `0`.

### Line 30

```python

```

Inside `MeasurementTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 31

```python
    def test_nearly_vertical_lip_is_rejected(self):
```

Inside `MeasurementTests`: Define `test_nearly_vertical_lip_is_rejected(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 32

```python
        with self.assertRaises(ValueError):
```

Inside `test_nearly_vertical_lip_is_rejected`: Enter managed resources: `self.assertRaises`: assert this expected test outcome; a mismatch fails the test. Arguments: `ValueError`. The resources are closed or restored when this block ends, including after errors.

### Line 33

```python
            measure_height((100, 400), (102, 500), (101, 200))
```

Inside `test_nearly_vertical_lip_is_rejected`: Run this operation: `measure_height`: interpolate the lip at the hip X coordinate and calculate a signed pixel gap. Arguments: tuple containing `100`; `400`; tuple containing `102`; `500`; tuple containing `101`; `200`.

### Line 34

```python

```

Inside `MeasurementTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 35

```python
    def test_hip_outside_segment_is_rejected(self):
```

Inside `MeasurementTests`: Define `test_hip_outside_segment_is_rejected(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 36

```python
        with self.assertRaises(ValueError):
```

Inside `test_hip_outside_segment_is_rejected`: Enter managed resources: `self.assertRaises`: assert this expected test outcome; a mismatch fails the test. Arguments: `ValueError`. The resources are closed or restored when this block ends, including after errors.

### Line 37

```python
            measure_height((100, 400), (800, 400), (900, 160))
```

Inside `test_hip_outside_segment_is_rejected`: Run this operation: `measure_height`: interpolate the lip at the hip X coordinate and calculate a signed pixel gap. Arguments: tuple containing `100`; `400`; tuple containing `800`; `400`; tuple containing `900`; `160`.

### Line 38

```python

```

Inside `MeasurementTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 39

```python
    def test_invalid_scales_are_rejected(self):
```

Inside `MeasurementTests`: Define `test_invalid_scales_are_rejected(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 40

```python
        for scale in (0, -1, float('nan'), float('inf')):
```

Inside `test_invalid_scales_are_rejected`: Repeat the following indented block for each `scale` from tuple containing `0`; negative `1`; `float`: convert a value to a decimal number. Arguments: `'nan'`; `float`: convert a value to a decimal number. Arguments: `'inf'`. Tuple targets unpack each loop item.

### Line 41

```python
            with self.subTest(scale=scale):
```

Inside `test_invalid_scales_are_rejected`: Enter managed resources: `self.subTest`: call this function with the supplied arguments. Arguments: scale = `scale`. The resources are closed or restored when this block ends, including after errors.

### Line 42

```python
                with self.assertRaises(ValueError):
```

Inside `test_invalid_scales_are_rejected`: Enter managed resources: `self.assertRaises`: assert this expected test outcome; a mismatch fails the test. Arguments: `ValueError`. The resources are closed or restored when this block ends, including after errors.

### Line 43

```python
                    measure_height((100, 400), (800, 400), (450, 160), scale)
```

Inside `test_invalid_scales_are_rejected`: Run this operation: `measure_height`: interpolate the lip at the hip X coordinate and calculate a signed pixel gap. Arguments: tuple containing `100`; `400`; tuple containing `800`; `400`; tuple containing `450`; `160`; `scale`.

### Line 44

```python

```

Inside `MeasurementTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 45

```python
    def test_nonfinite_point_is_rejected(self):
```

Inside `MeasurementTests`: Define `test_nonfinite_point_is_rejected(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 46

```python
        with self.assertRaises(ValueError):
```

Inside `test_nonfinite_point_is_rejected`: Enter managed resources: `self.assertRaises`: assert this expected test outcome; a mismatch fails the test. Arguments: `ValueError`. The resources are closed or restored when this block ends, including after errors.

### Line 47

```python
            measure_height((100, 400), (800, 400), (float('nan'), 160))
```

Inside `test_nonfinite_point_is_rejected`: Run this operation: `measure_height`: interpolate the lip at the hip X coordinate and calculate a signed pixel gap. Arguments: tuple containing `100`; `400`; tuple containing `800`; `400`; tuple containing `float`: convert a value to a decimal number. Arguments: `'nan'`; `160`.

### Line 48

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 49

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 50

```python
if __name__ == '__main__':
```

Run the indented block only when this condition is true: `__name__` equals `'__main__'`. Other branches handle the remaining case.

### Line 51

```python
    unittest.main()
```

Run this operation: `unittest.main`: discover and run this file's test cases. No arguments are supplied.

## test_analysis.py

Source SHA-256: `ab3d64cbc75f93634ef7c0ecd426fd5ffac4f2ce8a502a25ba884a5be9730acd`

### Line 1

```python
"""Check detection geometry, jump grouping, and saved video sessions."""
```

Documentation string: Check detection geometry, jump grouping, and saved video sessions. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 2

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 3

```python
import json
```

Import modules: json. Their functions become available through those module names.

### Line 4

```python
import tempfile
```

Import modules: tempfile. Their functions become available through those module names.

### Line 5

```python
import unittest
```

Import modules: unittest. Their functions become available through those module names.

### Line 6

```python
from pathlib import Path
```

Import Path from `pathlib`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 7

```python
from unittest.mock import patch
```

Import patch from `unittest.mock`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 8

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 9

```python
import cv2
```

Import modules: cv2. Their functions become available through those module names.

### Line 10

```python
import numpy as np
```

Import modules: numpy under the short name np. Their functions become available through those module names.

### Line 11

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 12

```python
from analysis import analyse, export_csv, find_jumps
```

Import analyse, export_csv, find_jumps from `analysis`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 13

```python
from vision import PoseDetector, choose_athlete, find_lip, motion_field, motion_regions
```

Import PoseDetector, choose_athlete, find_lip, motion_field, motion_regions from `vision`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 14

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 15

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 16

```python
def person(x=160, y=100):
```

Define `person(x=160, y=100)`. Its job: provide this reusable operation The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 17

```python
    return dict(box=[x - 20, y - 30, 40, 60], hip=[x, y], score=0.9, hip_score=0.9, points=[[0, 0, 0] for _ in range(17)], ambiguous=False)
```

Inside `person`: End this function now and send back `dict`: create a dictionary from the named fields. Arguments: box = list containing (`x` minus `20`); (`y` minus `30`); `40`; `60`; hip = list containing `x`; `y`; score = `0.9`; hip_score = `0.9`; points = produce list containing `0`; `0`; `0`, for each _ in `range`: produce integer loop positions, excluding the upper bound. Arguments: `17`; ambiguous = `False`. A bare return sends None.

### Line 18

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 19

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 20

```python
def sample(second, gap, cut=False):
```

Define `sample(second, gap, cut=False)`. Its job: provide this reusable operation The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 21

```python
    return dict(time=second, frame=round(second * 10), height_px=gap, person=person(), lip=dict(extrapolated=False), confidence=0.8, cut=cut)
```

Inside `sample`: End this function now and send back `dict`: create a dictionary from the named fields. Arguments: time = `second`; frame = `round`: round a number to the requested precision. Arguments: (`second` times `10`); height_px = `gap`; person = `person`: call this function with the supplied arguments. No arguments are supplied; lip = `dict`: create a dictionary from the named fields. Arguments: extrapolated = `False`; confidence = `0.8`; cut = `cut`. A bare return sends None.

### Line 22

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 23

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 24

```python
class JumpTests(unittest.TestCase):
```

Define the `JumpTests` class, inheriting from unittest.TestCase. A unittest test class collects related test cases.

### Line 25

```python
    def test_missing_evidence_does_not_become_zero(self):
```

Inside `JumpTests`: Define `test_missing_evidence_does_not_become_zero(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 26

```python
        samples = [sample(0, None), sample(1, -10), sample(2, 20)]
```

Inside `test_missing_evidence_does_not_become_zero`: Store the result in `samples`: list containing `sample`: call this function with the supplied arguments. Arguments: `0`; `None`; `sample`: call this function with the supplied arguments. Arguments: `1`; negative `10`; `sample`: call this function with the supplied arguments. Arguments: `2`; `20`. This is assignment, not an equality check.

### Line 27

```python
        self.assertEqual(find_jumps(samples, 10), [])
```

Inside `test_missing_evidence_does_not_become_zero`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `find_jumps`: group positive samples, require below-lip takeoff evidence, reject drop-ins, and number riding sequences. Arguments: `samples`; `10`; an empty list `[]`.

### Line 28

```python

```

Inside `JumpTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 29

```python
    def test_brief_gap_is_bridged_and_long_gap_splits(self):
```

Inside `JumpTests`: Define `test_brief_gap_is_bridged_and_long_gap_splits(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 30

```python
        samples = [sample(-0.1, -20), sample(0, 20), sample(0.1, 30), sample(0.2, None), sample(0.3, 25), sample(0.8, -20), sample(1, 20), sample(1.1, 30)]
```

Inside `test_brief_gap_is_bridged_and_long_gap_splits`: Store the result in `samples`: list containing `sample`: call this function with the supplied arguments. Arguments: negative `0.1`; negative `20`; `sample`: call this function with the supplied arguments. Arguments: `0`; `20`; `sample`: call this function with the supplied arguments. Arguments: `0.1`; `30`; `sample`: call this function with the supplied arguments. Arguments: `0.2`; `None`; `sample`: call this function with the supplied arguments. Arguments: `0.3`; `25`; `sample`: call this function with the supplied arguments. Arguments: `0.8`; negative `20`; `sample`: call this function with the supplied arguments. Arguments: `1`; `20`; `sample`: call this function with the supplied arguments. Arguments: `1.1`; `30`. This is assignment, not an equality check.

### Line 31

```python
        jumps = find_jumps(samples, 10)
```

Inside `test_brief_gap_is_bridged_and_long_gap_splits`: Store the result in `jumps`: `find_jumps`: group positive samples, require below-lip takeoff evidence, reject drop-ins, and number riding sequences. Arguments: `samples`; `10`. This is assignment, not an equality check.

### Line 32

```python
        self.assertEqual(len(jumps), 2)
```

Inside `test_brief_gap_is_bridged_and_long_gap_splits`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `len`: count items. Arguments: `jumps`; `2`.

### Line 33

```python
        self.assertEqual(jumps[0]['end'], 0.3)
```

Inside `test_brief_gap_is_bridged_and_long_gap_splits`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `jumps[0]['end']`; `0.3`.

### Line 34

```python
        self.assertIsNone(jumps[0]['height_m'])
```

Inside `test_brief_gap_is_bridged_and_long_gap_splits`: Run this operation: `self.assertIsNone`: assert this expected test outcome; a mismatch fails the test. Arguments: `jumps[0]['height_m']`.

### Line 35

```python
        self.assertFalse(jumps[0]['reviewed'])
```

Inside `test_brief_gap_is_bridged_and_long_gap_splits`: Run this operation: `self.assertFalse`: assert this expected test outcome; a mismatch fails the test. Arguments: `jumps[0]['reviewed']`.

### Line 36

```python

```

Inside `JumpTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 37

```python
    def test_camera_cut_splits_adjacent_candidates(self):
```

Inside `JumpTests`: Define `test_camera_cut_splits_adjacent_candidates(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 38

```python
        samples = [sample(-0.1, -20), sample(0, 20), sample(0.1, 30), sample(0.2, -20, True), sample(0.3, 40), sample(0.4, 35)]
```

Inside `test_camera_cut_splits_adjacent_candidates`: Store the result in `samples`: list containing `sample`: call this function with the supplied arguments. Arguments: negative `0.1`; negative `20`; `sample`: call this function with the supplied arguments. Arguments: `0`; `20`; `sample`: call this function with the supplied arguments. Arguments: `0.1`; `30`; `sample`: call this function with the supplied arguments. Arguments: `0.2`; negative `20`; `True`; `sample`: call this function with the supplied arguments. Arguments: `0.3`; `40`; `sample`: call this function with the supplied arguments. Arguments: `0.4`; `35`. This is assignment, not an equality check.

### Line 39

```python
        self.assertEqual(len(find_jumps(samples, 10)), 2)
```

Inside `test_camera_cut_splits_adjacent_candidates`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `len`: count items. Arguments: `find_jumps`: group positive samples, require below-lip takeoff evidence, reject drop-ins, and number riding sequences. Arguments: `samples`; `10`; `2`.

### Line 40

```python

```

Inside `JumpTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 41

```python
    def test_single_spike_is_not_selected_as_peak(self):
```

Inside `JumpTests`: Define `test_single_spike_is_not_selected_as_peak(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 42

```python
        samples = [sample(i / 10, gap) for i, gap in enumerate([-20, 20, 30, 500, 40, 20])]
```

Inside `test_single_spike_is_not_selected_as_peak`: Store the result in `samples`: produce `sample`: call this function with the supplied arguments. Arguments: (`i` divided by `10`); `gap`, for each (i, gap) in `enumerate`: provide both each item's index and its value. Arguments: list containing negative `20`; `20`; `30`; `500`; `40`; `20`. This is assignment, not an equality check.

### Line 43

```python
        self.assertEqual(find_jumps(samples, 10)[0]['height_px'], 40)
```

Inside `test_single_spike_is_not_selected_as_peak`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `find_jumps(samples, 10)[0]['height_px']`; `40`.

### Line 44

```python

```

Inside `JumpTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 45

```python
    def test_missing_person_cannot_be_a_jump(self):
```

Inside `JumpTests`: Define `test_missing_person_cannot_be_a_jump(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 46

```python
        item = sample(0, 20)
```

Inside `test_missing_person_cannot_be_a_jump`: Store the result in `item`: `sample`: call this function with the supplied arguments. Arguments: `0`; `20`. This is assignment, not an equality check.

### Line 47

```python
        item['person'] = None
```

Inside `test_missing_person_cannot_be_a_jump`: Store the result in `item['person']`: `None`. This is assignment, not an equality check.

### Line 48

```python
        self.assertEqual(find_jumps([item], 6), [])
```

Inside `test_missing_person_cannot_be_a_jump`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `find_jumps`: group positive samples, require below-lip takeoff evidence, reject drop-ins, and number riding sequences. Arguments: list containing `item`; `6`; an empty list `[]`.

### Line 49

```python

```

Inside `JumpTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 50

```python
    def test_initial_drop_in_is_rejected_but_later_takeoff_counts(self):
```

Inside `JumpTests`: Define `test_initial_drop_in_is_rejected_but_later_takeoff_counts(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 51

```python
        samples = [sample(i / 10, gap) for i, gap in enumerate([60, 40, 20, -30, -50, 20, 60, 30])]
```

Inside `test_initial_drop_in_is_rejected_but_later_takeoff_counts`: Store the result in `samples`: produce `sample`: call this function with the supplied arguments. Arguments: (`i` divided by `10`); `gap`, for each (i, gap) in `enumerate`: provide both each item's index and its value. Arguments: list containing `60`; `40`; `20`; negative `30`; negative `50`; `20`; `60`; `30`. This is assignment, not an equality check.

### Line 52

```python
        rejected = []
```

Inside `test_initial_drop_in_is_rejected_but_later_takeoff_counts`: Store the result in `rejected`: an empty list `[]`. This is assignment, not an equality check.

### Line 53

```python
        jumps = find_jumps(samples, 10, rejected)
```

Inside `test_initial_drop_in_is_rejected_but_later_takeoff_counts`: Store the result in `jumps`: `find_jumps`: group positive samples, require below-lip takeoff evidence, reject drop-ins, and number riding sequences. Arguments: `samples`; `10`; `rejected`. This is assignment, not an equality check.

### Line 54

```python
        self.assertEqual(len(jumps), 1)
```

Inside `test_initial_drop_in_is_rejected_but_later_takeoff_counts`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `len`: count items. Arguments: `jumps`; `1`.

### Line 55

```python
        self.assertEqual(jumps[0]['start'], 0.5)
```

Inside `test_initial_drop_in_is_rejected_but_later_takeoff_counts`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `jumps[0]['start']`; `0.5`.

### Line 56

```python
        self.assertEqual(len(rejected), 1)
```

Inside `test_initial_drop_in_is_rejected_but_later_takeoff_counts`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `len`: count items. Arguments: `rejected`; `1`.

### Line 57

```python

```

Inside `JumpTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 58

```python
    def test_cut_does_not_reuse_takeoff_from_previous_shot(self):
```

Inside `JumpTests`: Define `test_cut_does_not_reuse_takeoff_from_previous_shot(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 59

```python
        samples = [sample(0, -50), sample(0.1, 40, True), sample(0.2, 60)]
```

Inside `test_cut_does_not_reuse_takeoff_from_previous_shot`: Store the result in `samples`: list containing `sample`: call this function with the supplied arguments. Arguments: `0`; negative `50`; `sample`: call this function with the supplied arguments. Arguments: `0.1`; `40`; `True`; `sample`: call this function with the supplied arguments. Arguments: `0.2`; `60`. This is assignment, not an equality check.

### Line 60

```python
        self.assertEqual(find_jumps(samples, 10), [])
```

Inside `test_cut_does_not_reuse_takeoff_from_previous_shot`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `find_jumps`: group positive samples, require below-lip takeoff evidence, reject drop-ins, and number riding sequences. Arguments: `samples`; `10`; an empty list `[]`.

### Line 61

```python

```

Inside `JumpTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 62

```python
    def test_long_pause_starts_another_run(self):
```

Inside `JumpTests`: Define `test_long_pause_starts_another_run(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 63

```python
        samples = [sample(0, -30), sample(0.1, 20), sample(0.2, 40), sample(30, -30), sample(30.1, 20), sample(30.2, 40)]
```

Inside `test_long_pause_starts_another_run`: Store the result in `samples`: list containing `sample`: call this function with the supplied arguments. Arguments: `0`; negative `30`; `sample`: call this function with the supplied arguments. Arguments: `0.1`; `20`; `sample`: call this function with the supplied arguments. Arguments: `0.2`; `40`; `sample`: call this function with the supplied arguments. Arguments: `30`; negative `30`; `sample`: call this function with the supplied arguments. Arguments: `30.1`; `20`; `sample`: call this function with the supplied arguments. Arguments: `30.2`; `40`. This is assignment, not an equality check.

### Line 64

```python
        jumps = find_jumps(samples, 10)
```

Inside `test_long_pause_starts_another_run`: Store the result in `jumps`: `find_jumps`: group positive samples, require below-lip takeoff evidence, reject drop-ins, and number riding sequences. Arguments: `samples`; `10`. This is assignment, not an equality check.

### Line 65

```python
        self.assertEqual([(item['run'], item['jump_in_run']) for item in jumps], [(1, 1), (2, 1)])
```

Inside `test_long_pause_starts_another_run`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: produce tuple containing `item['run']`; `item['jump_in_run']`, for each item in `jumps`; list containing tuple containing `1`; `1`; tuple containing `2`; `1`.

### Line 66

```python

```

Inside `JumpTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 67

```python
    def test_standing_above_lip_is_not_a_jump(self):
```

Inside `JumpTests`: Define `test_standing_above_lip_is_not_a_jump(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 68

```python
        samples = [sample(i, 60) for i in range(10)]
```

Inside `test_standing_above_lip_is_not_a_jump`: Store the result in `samples`: produce `sample`: call this function with the supplied arguments. Arguments: `i`; `60`, for each i in `range`: produce integer loop positions, excluding the upper bound. Arguments: `10`. This is assignment, not an equality check.

### Line 69

```python
        self.assertEqual(find_jumps(samples, 2), [])
```

Inside `test_standing_above_lip_is_not_a_jump`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `find_jumps`: group positive samples, require below-lip takeoff evidence, reject drop-ins, and number riding sequences. Arguments: `samples`; `2`; an empty list `[]`.

### Line 70

```python

```

Inside `JumpTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 71

```python
    def test_fast_scan_preserves_a_strong_single_frame_candidate(self):
```

Inside `JumpTests`: Define `test_fast_scan_preserves_a_strong_single_frame_candidate(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 72

```python
        items = [sample(0, -50), sample(0.5, 60), sample(1, -30)]
```

Inside `test_fast_scan_preserves_a_strong_single_frame_candidate`: Store the result in `items`: list containing `sample`: call this function with the supplied arguments. Arguments: `0`; negative `50`; `sample`: call this function with the supplied arguments. Arguments: `0.5`; `60`; `sample`: call this function with the supplied arguments. Arguments: `1`; negative `30`. This is assignment, not an equality check.

### Line 73

```python
        items[1]['person']['motion'] = 0.9
```

Inside `test_fast_scan_preserves_a_strong_single_frame_candidate`: Store the result in `items[1]['person']['motion']`: `0.9`. This is assignment, not an equality check.

### Line 74

```python
        jumps = find_jumps(items, 2)
```

Inside `test_fast_scan_preserves_a_strong_single_frame_candidate`: Store the result in `jumps`: `find_jumps`: group positive samples, require below-lip takeoff evidence, reject drop-ins, and number riding sequences. Arguments: `items`; `2`. This is assignment, not an equality check.

### Line 75

```python
        self.assertEqual(len(jumps), 1)
```

Inside `test_fast_scan_preserves_a_strong_single_frame_candidate`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `len`: count items. Arguments: `jumps`; `1`.

### Line 76

```python
        self.assertTrue(any('Only one sampled frame' in reason for reason in jumps[0]['reasons']))
```

Inside `test_fast_scan_preserves_a_strong_single_frame_candidate`: Run this operation: `self.assertTrue`: assert this expected test outcome; a mismatch fails the test. Arguments: `any`: check whether at least one supplied condition is true. Arguments: produce `'Only one sampled frame'` is in `reason`, for each reason in `jumps[0]['reasons']`.

### Line 77

```python
        self.assertEqual(find_jumps(items, 6), [])
```

Inside `test_fast_scan_preserves_a_strong_single_frame_candidate`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `find_jumps`: group positive samples, require below-lip takeoff evidence, reject drop-ins, and number riding sequences. Arguments: `items`; `6`; an empty list `[]`.

### Line 78

```python

```

Inside `JumpTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 79

```python
    def test_weak_wrong_person_gap_does_not_split_one_jump(self):
```

Inside `JumpTests`: Define `test_weak_wrong_person_gap_does_not_split_one_jump(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 80

```python
        items = [sample(0, -30), sample(0.1, 20), sample(0.2, 40), sample(0.3, -40), sample(0.4, 60), sample(0.5, 20)]
```

Inside `test_weak_wrong_person_gap_does_not_split_one_jump`: Store the result in `items`: list containing `sample`: call this function with the supplied arguments. Arguments: `0`; negative `30`; `sample`: call this function with the supplied arguments. Arguments: `0.1`; `20`; `sample`: call this function with the supplied arguments. Arguments: `0.2`; `40`; `sample`: call this function with the supplied arguments. Arguments: `0.3`; negative `40`; `sample`: call this function with the supplied arguments. Arguments: `0.4`; `60`; `sample`: call this function with the supplied arguments. Arguments: `0.5`; `20`. This is assignment, not an equality check.

### Line 81

```python
        items[3]['confidence'] = 0.1
```

Inside `test_weak_wrong_person_gap_does_not_split_one_jump`: Store the result in `items[3]['confidence']`: `0.1`. This is assignment, not an equality check.

### Line 82

```python
        self.assertEqual(len(find_jumps(items, 10)), 1)
```

Inside `test_weak_wrong_person_gap_does_not_split_one_jump`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `len`: count items. Arguments: `find_jumps`: group positive samples, require below-lip takeoff evidence, reject drop-ins, and number riding sequences. Arguments: `items`; `10`; `1`.

### Line 83

```python

```

Inside `JumpTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 84

```python
    def test_stationary_peak_is_rejected_and_logged(self):
```

Inside `JumpTests`: Define `test_stationary_peak_is_rejected_and_logged(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 85

```python
        items = [sample(0, -30), sample(0.1, 20), sample(0.2, 40)]
```

Inside `test_stationary_peak_is_rejected_and_logged`: Store the result in `items`: list containing `sample`: call this function with the supplied arguments. Arguments: `0`; negative `30`; `sample`: call this function with the supplied arguments. Arguments: `0.1`; `20`; `sample`: call this function with the supplied arguments. Arguments: `0.2`; `40`. This is assignment, not an equality check.

### Line 86

```python
        for item in items:
```

Inside `test_stationary_peak_is_rejected_and_logged`: Repeat the following indented block for each `item` from `items`. Tuple targets unpack each loop item.

### Line 87

```python
            item['person']['motion'] = 0.01
```

Inside `test_stationary_peak_is_rejected_and_logged`: Store the result in `item['person']['motion']`: `0.01`. This is assignment, not an equality check.

### Line 88

```python
        rejected = []
```

Inside `test_stationary_peak_is_rejected_and_logged`: Store the result in `rejected`: an empty list `[]`. This is assignment, not an equality check.

### Line 89

```python
        self.assertEqual(find_jumps(items, 10, rejected), [])
```

Inside `test_stationary_peak_is_rejected_and_logged`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `find_jumps`: group positive samples, require below-lip takeoff evidence, reject drop-ins, and number riding sequences. Arguments: `items`; `10`; `rejected`; an empty list `[]`.

### Line 90

```python
        self.assertEqual(len(rejected), 1)
```

Inside `test_stationary_peak_is_rejected_and_logged`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `len`: count items. Arguments: `rejected`; `1`.

### Line 91

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 92

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 93

```python
class VisionTests(unittest.TestCase):
```

Define the `VisionTests` class, inheriting from unittest.TestCase. A unittest test class collects related test cases.

### Line 94

```python
    def test_lip_fit_tracks_a_sloping_blue_boundary(self):
```

Inside `VisionTests`: Define `test_lip_fit_tracks_a_sloping_blue_boundary(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 95

```python
        frame = np.full((240, 320, 3), 245, dtype=np.uint8)
```

Inside `test_lip_fit_tracks_a_sloping_blue_boundary`: Store the result in `frame`: `np.full`: create an array filled with a specified value. Arguments: tuple containing `240`; `320`; `3`; `245`; dtype = `np.uint8`. This is assignment, not an equality check.

### Line 96

```python
        cv2.line(frame, (20, 140), (300, 196), (255, 180, 30), 8)
```

Inside `test_lip_fit_tracks_a_sloping_blue_boundary`: Run this operation: `cv2.line`: draw a line on the supplied image. Arguments: `frame`; tuple containing `20`; `140`; tuple containing `300`; `196`; tuple containing `255`; `180`; `30`; `8`.

### Line 97

```python
        lip = find_lip(frame, [160, 80], [140, 50, 40, 60])
```

Inside `test_lip_fit_tracks_a_sloping_blue_boundary`: Store the result in `lip`: `find_lip`: find supporting blue pixels near the hip and fit a short robust reference line. Arguments: `frame`; list containing `160`; `80`; list containing `140`; `50`; `40`; `60`. This is assignment, not an equality check.

### Line 98

```python
        self.assertIsNotNone(lip)
```

Inside `test_lip_fit_tracks_a_sloping_blue_boundary`: Run this operation: `self.assertIsNotNone`: assert this expected test outcome; a mismatch fails the test. Arguments: `lip`.

### Line 99

```python
        self.assertAlmostEqual(lip['y'], 164, delta=5)
```

Inside `test_lip_fit_tracks_a_sloping_blue_boundary`: Run this operation: `self.assertAlmostEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `lip['y']`; `164`; delta = `5`.

### Line 100

```python

```

Inside `VisionTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 101

```python
    def test_white_frame_has_no_lip(self):
```

Inside `VisionTests`: Define `test_white_frame_has_no_lip(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 102

```python
        self.assertIsNone(find_lip(np.full((240, 320, 3), 255, dtype=np.uint8), [160, 80], [140, 50, 40, 60]))
```

Inside `test_white_frame_has_no_lip`: Run this operation: `self.assertIsNone`: assert this expected test outcome; a mismatch fails the test. Arguments: `find_lip`: find supporting blue pixels near the hip and fit a short robust reference line. Arguments: `np.full`: create an array filled with a specified value. Arguments: tuple containing `240`; `320`; `3`; `255`; dtype = `np.uint8`; list containing `160`; `80`; list containing `140`; `50`; `40`; `60`.

### Line 103

```python

```

Inside `VisionTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 104

```python
    def test_continuity_prefers_the_previous_athlete(self):
```

Inside `VisionTests`: Define `test_continuity_prefers_the_previous_athlete(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 105

```python
        athlete, other = person(145), person(290)
```

Inside `test_continuity_prefers_the_previous_athlete`: Store the result in `(athlete, other)`: tuple containing `person`: call this function with the supplied arguments. Arguments: `145`; `person`: call this function with the supplied arguments. Arguments: `290`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 106

```python
        self.assertEqual(choose_athlete([other, athlete], (240, 320, 3), person(140))['hip'], athlete['hip'])
```

Inside `test_continuity_prefers_the_previous_athlete`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `choose_athlete([other, athlete], (240, 320, 3), person(140))['hip']`; `athlete['hip']`.

### Line 107

```python

```

Inside `VisionTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 108

```python
    def test_motion_can_release_a_stationary_spectator(self):
```

Inside `VisionTests`: Define `test_motion_can_release_a_stationary_spectator(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 109

```python
        spectator, athlete = person(145), person(170)
```

Inside `test_motion_can_release_a_stationary_spectator`: Store the result in `(spectator, athlete)`: tuple containing `person`: call this function with the supplied arguments. Arguments: `145`; `person`: call this function with the supplied arguments. Arguments: `170`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 110

```python
        spectator.update(score=0.95, motion=0)
```

Inside `test_motion_can_release_a_stationary_spectator`: Run this operation: `spectator.update`: replace or add the supplied named fields. Arguments: score = `0.95`; motion = `0`.

### Line 111

```python
        athlete.update(score=0.65, motion=0.9)
```

Inside `test_motion_can_release_a_stationary_spectator`: Run this operation: `athlete.update`: replace or add the supplied named fields. Arguments: score = `0.65`; motion = `0.9`.

### Line 112

```python
        self.assertEqual(choose_athlete([spectator, athlete], (240, 320, 3), spectator)['hip'], athlete['hip'])
```

Inside `test_motion_can_release_a_stationary_spectator`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `choose_athlete([spectator, athlete], (240, 320, 3), spectator)['hip']`; `athlete['hip']`.

### Line 113

```python

```

Inside `VisionTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 114

```python
    def test_crop_rotation_restores_hip_and_box(self):
```

Inside `VisionTests`: Define `test_crop_rotation_restores_hip_and_box(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 115

```python
        detected = person(20, 30)
```

Inside `test_crop_rotation_restores_hip_and_box`: Store the result in `detected`: `person`: call this function with the supplied arguments. Arguments: `20`; `30`. This is assignment, not an equality check.

### Line 116

```python
        PoseDetector.restore_person(detected, 1, 200, 200, 430, 50)
```

Inside `test_crop_rotation_restores_hip_and_box`: Run this operation: `PoseDetector.restore_person`: reverse crop rotation and offset for boxes, hips, and body landmarks. Arguments: `detected`; `1`; `200`; `200`; `430`; `50`.

### Line 117

```python
        self.assertEqual(detected['hip'], [599, 70])
```

Inside `test_crop_rotation_restores_hip_and_box`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `detected['hip']`; list containing `599`; `70`.

### Line 118

```python
        self.assertGreater(detected['box'][2], 0)
```

Inside `test_crop_rotation_restores_hip_and_box`: Run this operation: `self.assertGreater`: assert this expected test outcome; a mismatch fails the test. Arguments: `detected['box'][2]`; `0`.

### Line 119

```python

```

Inside `VisionTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 120

```python
    def test_motion_region_needs_multiple_moving_features(self):
```

Inside `VisionTests`: Define `test_motion_region_needs_multiple_moving_features(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 121

```python
        field = dict(size=(640, 360), points=np.array([[300., 100.]]), residual=np.array([20.]), baseline=0., ratio=2/3)
```

Inside `test_motion_region_needs_multiple_moving_features`: Store the result in `field`: `dict`: create a dictionary from the named fields. Arguments: size = tuple containing `640`; `360`; points = `np.array`: put the supplied values into a numerical array. Arguments: list containing list containing `300.0`; `100.0`; residual = `np.array`: put the supplied values into a numerical array. Arguments: list containing `20.0`; baseline = `0.0`; ratio = (`2` divided by `3`). This is assignment, not an equality check.

### Line 122

```python
        self.assertEqual(motion_regions(field, (540, 960, 3)), [])
```

Inside `test_motion_region_needs_multiple_moving_features`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `motion_regions`: group strongly moving features and choose a magnified search region. Arguments: `field`; tuple containing `540`; `960`; `3`; an empty list `[]`.

### Line 123

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 124

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 125

```python
class SessionTests(unittest.TestCase):
```

Define the `SessionTests` class, inheriting from unittest.TestCase. A unittest test class collects related test cases.

### Line 126

```python
    def setUp(self):
```

Inside `SessionTests`: Define `setUp(self)`. Its job: prepare fresh temporary test inputs before each test The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 127

```python
        self.temporary = tempfile.TemporaryDirectory()
```

Inside `setUp`: Store the result in `self.temporary`: `tempfile.TemporaryDirectory`: create an isolated test folder that is later cleaned up. No arguments are supplied. This is assignment, not an equality check.

### Line 128

```python
        self.folder = Path(self.temporary.name)
```

Inside `setUp`: Store the result in `self.folder`: `Path`: create a filesystem path object. Arguments: `self.temporary.name`. This is assignment, not an equality check.

### Line 129

```python
        self.video = self.folder / 'input.mp4'
```

Inside `setUp`: Store the result in `self.video`: (`self.folder` divided by `'input.mp4'`). This is assignment, not an equality check.

### Line 130

```python
        writer = cv2.VideoWriter(str(self.video), cv2.VideoWriter_fourcc(*'mp4v'), 10, (320, 240))
```

Inside `setUp`: Store the result in `writer`: `cv2.VideoWriter`: create a video file encoder. Arguments: `str`: convert a value to text. Arguments: `self.video`; `cv2.VideoWriter_fourcc`: turn the four codec letters into OpenCV's codec identifier. Arguments: `*'mp4v'`; `10`; tuple containing `320`; `240`. This is assignment, not an equality check.

### Line 131

```python
        self.assertTrue(writer.isOpened())
```

Inside `setUp`: Run this operation: `self.assertTrue`: assert this expected test outcome; a mismatch fails the test. Arguments: `writer.isOpened`: check whether the video resource opened successfully. No arguments are supplied.

### Line 132

```python
        for index in range(30):
```

Inside `setUp`: Repeat the following indented block for each `index` from `range`: produce integer loop positions, excluding the upper bound. Arguments: `30`. Tuple targets unpack each loop item.

### Line 133

```python
            frame = np.full((240, 320, 3), 245, dtype=np.uint8)
```

Inside `setUp`: Store the result in `frame`: `np.full`: create an array filled with a specified value. Arguments: tuple containing `240`; `320`; `3`; `245`; dtype = `np.uint8`. This is assignment, not an equality check.

### Line 134

```python
            cv2.line(frame, (20, 160), (300, 160), (255, 180, 30), 8)
```

Inside `setUp`: Run this operation: `cv2.line`: draw a line on the supplied image. Arguments: `frame`; tuple containing `20`; `160`; tuple containing `300`; `160`; tuple containing `255`; `180`; `30`; `8`.

### Line 135

```python
            writer.write(frame)
```

Inside `setUp`: Run this operation: `writer.write`: write bytes or an encoded frame to the open output. Arguments: `frame`.

### Line 136

```python
        writer.release()
```

Inside `setUp`: Run this operation: `writer.release`: close the video reader or finalize the video writer. No arguments are supplied.

### Line 137

```python

```

Inside `SessionTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 138

```python
    def tearDown(self):
```

Inside `SessionTests`: Define `tearDown(self)`. Its job: remove the temporary test files after each test The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 139

```python
        self.temporary.cleanup()
```

Inside `tearDown`: Run this operation: `self.temporary.cleanup`: remove this temporary test folder. No arguments are supplied.

### Line 140

```python

```

Inside `SessionTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 141

```python
    def run_session(self, **settings):
```

Inside `SessionTests`: Define `run_session(self, **settings)`. Its job: run the real session pipeline with a predictable mocked person detector The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 142

```python
        with patch('analysis.PoseDetector') as detector:
```

Inside `run_session`: Enter managed resources: `patch`: replace a dependency temporarily inside a test. Arguments: `'analysis.PoseDetector'` stored as `detector`. The resources are closed or restored when this block ends, including after errors.

### Line 143

```python
            detector.return_value.detect.side_effect = [[person(160, 200)]] + [[person()]] * 30
```

Inside `run_session`: Store the result in `detector.return_value.detect.side_effect`: (list containing list containing `person`: call this function with the supplied arguments. Arguments: `160`; `200` plus (list containing list containing `person`: call this function with the supplied arguments. No arguments are supplied times `30`)). This is assignment, not an equality check.

### Line 144

```python
            return analyse(str(self.video), model_path='unused-in-this-mocked-test', folder=self.folder / 'session', sample_rate=5, **settings)
```

Inside `run_session`: End this function now and send back `analyse`: process the selected video range, store evidence, group candidates, and save outputs. Arguments: `str`: convert a value to text. Arguments: `self.video`; model_path = `'unused-in-this-mocked-test'`; folder = (`self.folder` divided by `'session'`); sample_rate = `5`; ** = `settings`. A bare return sends None.

### Line 145

```python

```

Inside `SessionTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 146

```python
    def test_range_export_and_review_video(self):
```

Inside `SessionTests`: Define `test_range_export_and_review_video(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 147

```python
        report = self.run_session(start=1, end=2)
```

Inside `test_range_export_and_review_video`: Store the result in `report`: `self.run_session`: run the real session pipeline with a predictable mocked person detector. Arguments: start = `1`; end = `2`. This is assignment, not an equality check.

### Line 148

```python
        self.assertTrue(report['complete'])
```

Inside `test_range_export_and_review_video`: Run this operation: `self.assertTrue`: assert this expected test outcome; a mismatch fails the test. Arguments: `report['complete']`.

### Line 149

```python
        self.assertEqual(len(report['samples']), 5)
```

Inside `test_range_export_and_review_video`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `len`: count items. Arguments: `report['samples']`; `5`.

### Line 150

```python
        self.assertEqual(report['samples'][0]['frame'], 10)
```

Inside `test_range_export_and_review_video`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `report['samples'][0]['frame']`; `10`.

### Line 151

```python
        self.assertLess(report['samples'][-1]['time'], 2)
```

Inside `test_range_export_and_review_video`: Run this operation: `self.assertLess`: assert this expected test outcome; a mismatch fails the test. Arguments: `report['samples'][-1]['time']`; `2`.

### Line 152

```python
        loaded = json.loads((self.folder / 'session/report.json').read_text())
```

Inside `test_range_export_and_review_video`: Store the result in `loaded`: `json.loads`: parse JSON text back into Python values. Arguments: `(self.folder / 'session/report.json').read_text`: read a complete text file with the selected encoding. No arguments are supplied. This is assignment, not an equality check.

### Line 153

```python
        self.assertEqual(loaded['state'], 'complete')
```

Inside `test_range_export_and_review_video`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `loaded['state']`; `'complete'`.

### Line 154

```python
        self.assertTrue((self.folder / 'session/jumps.csv').exists())
```

Inside `test_range_export_and_review_video`: Run this operation: `self.assertTrue`: assert this expected test outcome; a mismatch fails the test. Arguments: `(self.folder / 'session/jumps.csv').exists`: check whether this path currently exists. No arguments are supplied.

### Line 155

```python
        self.assertTrue((self.folder / 'session/skipped.csv').exists())
```

Inside `test_range_export_and_review_video`: Run this operation: `self.assertTrue`: assert this expected test outcome; a mismatch fails the test. Arguments: `(self.folder / 'session/skipped.csv').exists`: check whether this path currently exists. No arguments are supplied.

### Line 156

```python
        capture = cv2.VideoCapture(str(self.folder / 'session/review.mp4'))
```

Inside `test_range_export_and_review_video`: Store the result in `capture`: `cv2.VideoCapture`: create a video reader. Arguments: `str`: convert a value to text. Arguments: (`self.folder` divided by `'session/review.mp4'`). This is assignment, not an equality check.

### Line 157

```python
        self.assertTrue(capture.isOpened())
```

Inside `test_range_export_and_review_video`: Run this operation: `self.assertTrue`: assert this expected test outcome; a mismatch fails the test. Arguments: `capture.isOpened`: check whether the video resource opened successfully. No arguments are supplied.

### Line 158

```python
        self.assertEqual(int(capture.get(cv2.CAP_PROP_FRAME_COUNT)), 5)
```

Inside `test_range_export_and_review_video`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `int`: convert a value to a whole number. Arguments: `capture.get`: look up a dictionary field with an optional fallback, or read the named video property. Arguments: `cv2.CAP_PROP_FRAME_COUNT`; `5`.

### Line 159

```python
        capture.release()
```

Inside `test_range_export_and_review_video`: Run this operation: `capture.release`: close the video reader or finalize the video writer. No arguments are supplied.

### Line 160

```python
        report['jumps'][0].update(excluded=True, reviewed=True)
```

Inside `test_range_export_and_review_video`: Run this operation: `report['jumps'][0].update`: replace or add the supplied named fields. Arguments: excluded = `True`; reviewed = `True`.

### Line 161

```python
        export_csv(report, self.folder / 'export.csv')
```

Inside `test_range_export_and_review_video`: Run this operation: `export_csv`: write candidate rows including their review and exclusion flags. Arguments: `report`; (`self.folder` divided by `'export.csv'`).

### Line 162

```python
        self.assertIn('True,True', (self.folder / 'export.csv').read_text(encoding='utf-8-sig'))
```

Inside `test_range_export_and_review_video`: Run this operation: `self.assertIn`: assert this expected test outcome; a mismatch fails the test. Arguments: `'True,True'`; `(self.folder / 'export.csv').read_text`: read a complete text file with the selected encoding. Arguments: encoding = `'utf-8-sig'`.

### Line 163

```python

```

Inside `SessionTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 164

```python
    def test_stop_preserves_partial_results(self):
```

Inside `SessionTests`: Define `test_stop_preserves_partial_results(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 165

```python
        updates = []
```

Inside `test_stop_preserves_partial_results`: Store the result in `updates`: an empty list `[]`. This is assignment, not an equality check.

### Line 166

```python
        report = self.run_session(progress=updates.append, cancelled=lambda: len(updates) >= 2)
```

Inside `test_stop_preserves_partial_results`: Store the result in `report`: `self.run_session`: run the real session pipeline with a predictable mocked person detector. Arguments: progress = `updates.append`; cancelled = a short function taking `` and returning `len`: count items. Arguments: `updates` is at least `2`. This is assignment, not an equality check.

### Line 167

```python
        self.assertEqual(report['state'], 'stopped')
```

Inside `test_stop_preserves_partial_results`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `report['state']`; `'stopped'`.

### Line 168

```python
        self.assertFalse(report['complete'])
```

Inside `test_stop_preserves_partial_results`: Run this operation: `self.assertFalse`: assert this expected test outcome; a mismatch fails the test. Arguments: `report['complete']`.

### Line 169

```python
        self.assertGreater(len(report['samples']), 0)
```

Inside `test_stop_preserves_partial_results`: Run this operation: `self.assertGreater`: assert this expected test outcome; a mismatch fails the test. Arguments: `len`: count items. Arguments: `report['samples']`; `0`.

### Line 170

```python
        self.assertLess(len(report['samples']), 15)
```

Inside `test_stop_preserves_partial_results`: Run this operation: `self.assertLess`: assert this expected test outcome; a mismatch fails the test. Arguments: `len`: count items. Arguments: `report['samples']`; `15`.

### Line 171

```python
        self.assertTrue((self.folder / 'session/report.json').exists())
```

Inside `test_stop_preserves_partial_results`: Run this operation: `self.assertTrue`: assert this expected test outcome; a mismatch fails the test. Arguments: `(self.folder / 'session/report.json').exists`: check whether this path currently exists. No arguments are supplied.

### Line 172

```python

```

Inside `SessionTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 173

```python
    def test_invalid_range_is_rejected(self):
```

Inside `SessionTests`: Define `test_invalid_range_is_rejected(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 174

```python
        with self.assertRaises(ValueError):
```

Inside `test_invalid_range_is_rejected`: Enter managed resources: `self.assertRaises`: assert this expected test outcome; a mismatch fails the test. Arguments: `ValueError`. The resources are closed or restored when this block ends, including after errors.

### Line 175

```python
            self.run_session(start=2, end=1)
```

Inside `test_invalid_range_is_rejected`: Run this operation: `self.run_session`: run the real session pipeline with a predictable mocked person detector. Arguments: start = `2`; end = `1`.

### Line 176

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 177

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 178

```python
if __name__ == '__main__':
```

Run the indented block only when this condition is true: `__name__` equals `'__main__'`. Other branches handle the remaining case.

### Line 179

```python
    unittest.main()
```

Run this operation: `unittest.main`: discover and run this file's test cases. No arguments are supplied.

## test_app.py

Source SHA-256: `fdf81c75c87d562decb9d7de667e96090eace529afdce4d6855a3ce1d26d02da`

### Line 1

```python
"""Test native review actions without needing an interactive display."""
```

Documentation string: Test native review actions without needing an interactive display. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 2

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 3

```python
import os
```

Import modules: os. Their functions become available through those module names.

### Line 4

```python
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
```

Run this operation: `os.environ.setdefault`: call this function with the supplied arguments. Arguments: `'QT_QPA_PLATFORM'`; `'offscreen'`.

### Line 5

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 6

```python
import tempfile
```

Import modules: tempfile. Their functions become available through those module names.

### Line 7

```python
import unittest
```

Import modules: unittest. Their functions become available through those module names.

### Line 8

```python
from pathlib import Path
```

Import Path from `pathlib`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 9

```python
from unittest.mock import patch
```

Import patch from `unittest.mock`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 10

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 11

```python
import numpy as np
```

Import modules: numpy under the short name np. Their functions become available through those module names.

### Line 12

```python
from PySide6.QtWidgets import QApplication
```

Import QApplication from `PySide6.QtWidgets`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 13

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 14

```python
from app import MainWindow
```

Import MainWindow from `app`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 15

```python
from test_analysis import person, sample
```

Import person, sample from `test_analysis`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 16

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 17

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 18

```python
class ReviewTests(unittest.TestCase):
```

Define the `ReviewTests` class, inheriting from unittest.TestCase. A unittest test class collects related test cases.

### Line 19

```python
    @classmethod
```

Inside `ReviewTests`: Apply a decorator to the next method. `@classmethod` passes the class itself as cls instead of a particular object as self.

### Line 20

```python
    def setUpClass(cls):
```

Inside `ReviewTests`: Define `setUpClass(cls)`. Its job: prepare one Qt application for this test class The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 21

```python
        cls.application = QApplication.instance() or QApplication([])
```

Inside `setUpClass`: Store the result in `cls.application`: `QApplication.instance`: call this function with the supplied arguments. No arguments are supplied OR `QApplication`: create the Qt application and event loop owner. Arguments: an empty list `[]`. This is assignment, not an equality check.

### Line 22

```python

```

Inside `ReviewTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 23

```python
    def test_review_exclusion_scale_and_point_correction(self):
```

Inside `ReviewTests`: Define `test_review_exclusion_scale_and_point_correction(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 24

```python
        with tempfile.TemporaryDirectory() as temporary, patch.object(MainWindow, 'load_recent'), patch.object(MainWindow, 'save_recent'):
```

Inside `test_review_exclusion_scale_and_point_correction`: Enter managed resources: `tempfile.TemporaryDirectory`: create an isolated test folder that is later cleaned up. No arguments are supplied stored as `temporary`; `patch.object`: temporarily replace a method so the test avoids changing personal recent-session state. Arguments: `MainWindow`; `'load_recent'`; `patch.object`: temporarily replace a method so the test avoids changing personal recent-session state. Arguments: `MainWindow`; `'save_recent'`. The resources are closed or restored when this block ends, including after errors.

### Line 25

```python
            window = MainWindow()
```

Inside `test_review_exclusion_scale_and_point_correction`: Store the result in `window`: `MainWindow`: call this function with the supplied arguments. No arguments are supplied. This is assignment, not an equality check.

### Line 26

```python
            peak = sample(1, 60)
```

Inside `test_review_exclusion_scale_and_point_correction`: Store the result in `peak`: `sample`: call this function with the supplied arguments. Arguments: `1`; `60`. This is assignment, not an equality check.

### Line 27

```python
            peak['lip'].update(a=[20, 160], b=[300, 160], y=160)
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `peak['lip'].update`: replace or add the supplied named fields. Arguments: a = list containing `20`; `160`; b = list containing `300`; `160`; y = `160`.

### Line 28

```python
            jump = dict(id=1, start=0.8, end=1.2, peak_time=1, frame=10, height_px=60, height_m=None, scale=None, confidence=0.8, reviewed=False, excluded=False, reasons=[], sample_index=0)
```

Inside `test_review_exclusion_scale_and_point_correction`: Store the result in `jump`: `dict`: create a dictionary from the named fields. Arguments: id = `1`; start = `0.8`; end = `1.2`; peak_time = `1`; frame = `10`; height_px = `60`; height_m = `None`; scale = `None`; confidence = `0.8`; reviewed = `False`; excluded = `False`; reasons = an empty list `[]`; sample_index = `0`. This is assignment, not an equality check.

### Line 29

```python
            report = dict(version=2, source='test.mp4', folder=temporary, start=0, end=3, fps=10, samples=[peak], jumps=[jump], state='complete', complete=True)
```

Inside `test_review_exclusion_scale_and_point_correction`: Store the result in `report`: `dict`: create a dictionary from the named fields. Arguments: version = `2`; source = `'test.mp4'`; folder = `temporary`; start = `0`; end = `3`; fps = `10`; samples = list containing `peak`; jumps = list containing `jump`; state = `'complete'`; complete = `True`. This is assignment, not an equality check.

### Line 30

```python
            window.receive_report(report)
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `window.receive_report`: replace the displayed session and refresh its candidates and metrics. Arguments: `report`.

### Line 31

```python
            window.mark_reviewed()
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `window.mark_reviewed`: mark the selected candidate reviewed and restore it if previously excluded. No arguments are supplied.

### Line 32

```python
            self.assertTrue(jump['reviewed'])
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `self.assertTrue`: assert this expected test outcome; a mismatch fails the test. Arguments: `jump['reviewed']`.

### Line 33

```python
            window.exclude()
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `window.exclude`: mark a candidate excluded while retaining its row and evidence. No arguments are supplied.

### Line 34

```python
            self.assertTrue(jump['excluded'])
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `self.assertTrue`: assert this expected test outcome; a mismatch fails the test. Arguments: `jump['excluded']`.

### Line 35

```python
            window.correction_jump = jump
```

Inside `test_review_exclusion_scale_and_point_correction`: Store the result in `window.correction_jump`: `jump`. This is assignment, not an equality check.

### Line 36

```python
            window.reference_length.setValue(1)
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `window.reference_length.setValue`: set the numeric input or progress value. Arguments: `1`.

### Line 37

```python
            window.save_calibration([(160, 100), (160, 120)])
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `window.save_calibration`: validate a known vertical reference and save a metre estimate for this selected peak. Arguments: list containing tuple containing `160`; `100`; tuple containing `160`; `120`.

### Line 38

```python
            self.assertEqual(jump['height_m'], 3)
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `jump['height_m']`; `3`.

### Line 39

```python
            window.correction_jump = jump
```

Inside `test_review_exclusion_scale_and_point_correction`: Store the result in `window.correction_jump`: `jump`. This is assignment, not an equality check.

### Line 40

```python
            window.raw_frame = np.full((240, 320, 3), 255, dtype=np.uint8)
```

Inside `test_review_exclusion_scale_and_point_correction`: Store the result in `window.raw_frame`: `np.full`: create an array filled with a specified value. Arguments: tuple containing `240`; `320`; `3`; `255`; dtype = `np.uint8`. This is assignment, not an equality check.

### Line 41

```python
            window.correct_points([(20, 150), (300, 150), (160, 100)])
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `window.correct_points`: draw clicked points, validate geometry, and save a corrected or manual candidate. Arguments: list containing tuple containing `20`; `150`; tuple containing `300`; `150`; tuple containing `160`; `100`.

### Line 42

```python
            self.assertEqual(jump['height_px'], 50)
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `jump['height_px']`; `50`.

### Line 43

```python
            self.assertIsNone(jump['height_m'])
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `self.assertIsNone`: assert this expected test outcome; a mismatch fails the test. Arguments: `jump['height_m']`.

### Line 44

```python
            self.assertTrue((Path(temporary) / jump['snapshot']).exists())
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `self.assertTrue`: assert this expected test outcome; a mismatch fails the test. Arguments: `(Path(temporary) / jump['snapshot']).exists`: check whether this path currently exists. No arguments are supplied.

### Line 45

```python
            window.pending_manual = dict(time=2, frame=20)
```

Inside `test_review_exclusion_scale_and_point_correction`: Store the result in `window.pending_manual`: `dict`: create a dictionary from the named fields. Arguments: time = `2`; frame = `20`. This is assignment, not an equality check.

### Line 46

```python
            window.correct_points([(20, 150), (300, 150), (160, 90)])
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `window.correct_points`: draw clicked points, validate geometry, and save a corrected or manual candidate. Arguments: list containing tuple containing `20`; `150`; tuple containing `300`; `150`; tuple containing `160`; `90`.

### Line 47

```python
            self.assertEqual(len(report['jumps']), 2)
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `len`: count items. Arguments: `report['jumps']`; `2`.

### Line 48

```python
            self.assertTrue(report['jumps'][-1]['manual'])
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `self.assertTrue`: assert this expected test outcome; a mismatch fails the test. Arguments: `report['jumps'][-1]['manual']`.

### Line 49

```python
            self.assertEqual(report['jumps'][-1]['height_px'], 60)
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `report['jumps'][-1]['height_px']`; `60`.

### Line 50

```python
            window.resize(1100, 800)
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `window.resize`: request an initial window size. Arguments: `1100`; `800`.

### Line 51

```python
            window.show()
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `window.show`: make the window visible. No arguments are supplied.

### Line 52

```python
            self.application.processEvents()
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `self.application.processEvents`: let Qt deliver pending layout and paint events during the test. No arguments are supplied.

### Line 53

```python
            self.assertGreater(window.canvas.width(), 400)
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `self.assertGreater`: assert this expected test outcome; a mismatch fails the test. Arguments: `window.canvas.width`: read this widget's current width. No arguments are supplied; `400`.

### Line 54

```python
            window.close()
```

Inside `test_review_exclusion_scale_and_point_correction`: Run this operation: `window.close`: request that the window close. No arguments are supplied.

### Line 55

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 56

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 57

```python
if __name__ == '__main__':
```

Run the indented block only when this condition is true: `__name__` equals `'__main__'`. Other branches handle the remaining case.

### Line 58

```python
    unittest.main()
```

Run this operation: `unittest.main`: discover and run this file's test cases. No arguments are supplied.

## test_calibration.py

Source SHA-256: `40bed009c55efd232d2955f717533f623ed3988c797ce9ba0c29325221388c55`

### Line 1

```python
"""Verify the metre conversion and local vertical reference geometry."""
```

Documentation string: Verify the metre conversion and local vertical reference geometry. It describes this module, class, or function; it is not an action the user needs to perform.

### Line 2

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 3

```python
import unittest
```

Import modules: unittest. Their functions become available through those module names.

### Line 4

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 5

```python
from measurement import calibrate_height
```

Import calibrate_height from `measurement`. These names can then be used directly. Qt names beginning with Q are window, event, drawing, or control classes.

### Line 6

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 7

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 8

```python
class CalibrationTests(unittest.TestCase):
```

Define the `CalibrationTests` class, inheriting from unittest.TestCase. A unittest test class collects related test cases.

### Line 9

```python
    def test_known_vertical_reference(self):
```

Inside `CalibrationTests`: Define `test_known_vertical_reference(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 10

```python
        metres, scale, gap = calibrate_height((0, 150), (300, 150), (150, 90), (100, 80), (100, 100), 1)
```

Inside `test_known_vertical_reference`: Store the result in `(metres, scale, gap)`: `calibrate_height`: intersect the local vertical through the hip with the lip, then convert its signed distance using a known reference length. Arguments: tuple containing `0`; `150`; tuple containing `300`; `150`; tuple containing `150`; `90`; tuple containing `100`; `80`; tuple containing `100`; `100`; `1`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 11

```python
        self.assertEqual(metres, 3)
```

Inside `test_known_vertical_reference`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `metres`; `3`.

### Line 12

```python
        self.assertEqual(scale, 20)
```

Inside `test_known_vertical_reference`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `scale`; `20`.

### Line 13

```python
        self.assertEqual(gap, 60)
```

Inside `test_known_vertical_reference`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `gap`; `60`.

### Line 14

```python

```

Inside `CalibrationTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 15

```python
    def test_tilted_reference_uses_projected_vertical(self):
```

Inside `CalibrationTests`: Define `test_tilted_reference_uses_projected_vertical(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 16

```python
        metres, scale, gap = calibrate_height((0, 150), (300, 150), (100, 100), (100, 100), (130, 140), 2)
```

Inside `test_tilted_reference_uses_projected_vertical`: Store the result in `(metres, scale, gap)`: `calibrate_height`: intersect the local vertical through the hip with the lip, then convert its signed distance using a known reference length. Arguments: tuple containing `0`; `150`; tuple containing `300`; `150`; tuple containing `100`; `100`; tuple containing `100`; `100`; tuple containing `130`; `140`; `2`. Multiple names separated by commas unpack values in order. This is assignment, not an equality check.

### Line 17

```python
        self.assertAlmostEqual(gap, 62.5)
```

Inside `test_tilted_reference_uses_projected_vertical`: Run this operation: `self.assertAlmostEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `gap`; `62.5`.

### Line 18

```python
        self.assertEqual(scale, 25)
```

Inside `test_tilted_reference_uses_projected_vertical`: Run this operation: `self.assertEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `scale`; `25`.

### Line 19

```python
        self.assertAlmostEqual(metres, 2.5)
```

Inside `test_tilted_reference_uses_projected_vertical`: Run this operation: `self.assertAlmostEqual`: assert this expected test outcome; a mismatch fails the test. Arguments: `metres`; `2.5`.

### Line 20

```python

```

Inside `CalibrationTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 21

```python
    def test_reference_order_and_short_length_are_rejected(self):
```

Inside `CalibrationTests`: Define `test_reference_order_and_short_length_are_rejected(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 22

```python
        for top, bottom in [((0, 20), (0, 0)), ((0, 0), (0, 5))]:
```

Inside `test_reference_order_and_short_length_are_rejected`: Repeat the following indented block for each `(top, bottom)` from list containing tuple containing tuple containing `0`; `20`; tuple containing `0`; `0`; tuple containing tuple containing `0`; `0`; tuple containing `0`; `5`. Tuple targets unpack each loop item.

### Line 23

```python
            with self.assertRaises(ValueError):
```

Inside `test_reference_order_and_short_length_are_rejected`: Enter managed resources: `self.assertRaises`: assert this expected test outcome; a mismatch fails the test. Arguments: `ValueError`. The resources are closed or restored when this block ends, including after errors.

### Line 24

```python
                calibrate_height((0, 100), (200, 100), (100, 50), top, bottom, 1)
```

Inside `test_reference_order_and_short_length_are_rejected`: Run this operation: `calibrate_height`: intersect the local vertical through the hip with the lip, then convert its signed distance using a known reference length. Arguments: tuple containing `0`; `100`; tuple containing `200`; `100`; tuple containing `100`; `50`; `top`; `bottom`; `1`.

### Line 25

```python

```

Inside `CalibrationTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 26

```python
    def test_parallel_reference_is_rejected(self):
```

Inside `CalibrationTests`: Define `test_parallel_reference_is_rejected(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 27

```python
        with self.assertRaises(ValueError):
```

Inside `test_parallel_reference_is_rejected`: Enter managed resources: `self.assertRaises`: assert this expected test outcome; a mismatch fails the test. Arguments: `ValueError`. The resources are closed or restored when this block ends, including after errors.

### Line 28

```python
            calibrate_height((0, 100), (200, 120), (100, 50), (0, 0), (100, 10), 1)
```

Inside `test_parallel_reference_is_rejected`: Run this operation: `calibrate_height`: intersect the local vertical through the hip with the lip, then convert its signed distance using a known reference length. Arguments: tuple containing `0`; `100`; tuple containing `200`; `120`; tuple containing `100`; `50`; tuple containing `0`; `0`; tuple containing `100`; `10`; `1`.

### Line 29

```python

```

Inside `CalibrationTests`: Blank line. It separates related parts for readability and performs no operation.

### Line 30

```python
    def test_unknown_length_is_rejected(self):
```

Inside `CalibrationTests`: Define `test_unknown_length_is_rejected(self)`. Its job: run the named test case The body runs when the function is called, not when it is defined. `self` is the current object when present. Parameters after `=` have defaults.

### Line 31

```python
        for length in [0, -1, float('nan')]:
```

Inside `test_unknown_length_is_rejected`: Repeat the following indented block for each `length` from list containing `0`; negative `1`; `float`: convert a value to a decimal number. Arguments: `'nan'`. Tuple targets unpack each loop item.

### Line 32

```python
            with self.assertRaises(ValueError):
```

Inside `test_unknown_length_is_rejected`: Enter managed resources: `self.assertRaises`: assert this expected test outcome; a mismatch fails the test. Arguments: `ValueError`. The resources are closed or restored when this block ends, including after errors.

### Line 33

```python
                calibrate_height((0, 100), (200, 100), (100, 50), (0, 0), (0, 20), length)
```

Inside `test_unknown_length_is_rejected`: Run this operation: `calibrate_height`: intersect the local vertical through the hip with the lip, then convert its signed distance using a known reference length. Arguments: tuple containing `0`; `100`; tuple containing `200`; `100`; tuple containing `100`; `50`; tuple containing `0`; `0`; tuple containing `0`; `20`; `length`.

### Line 34

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 35

```python

```

Blank line. It separates related parts for readability and performs no operation.

### Line 36

```python
if __name__ == '__main__':
```

Run the indented block only when this condition is true: `__name__` equals `'__main__'`. Other branches handle the remaining case.

### Line 37

```python
    unittest.main()
```

Run this operation: `unittest.main`: discover and run this file's test cases. No arguments are supplied.

