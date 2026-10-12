# Every Python line explained

These line numbers match the files in this version. Read BEGINNER_GUIDE.md first if Python is new to you. Every line, including blank lines and docstrings, has an entry. A code block shows the exact line. The paragraph below it explains the purpose.

Python runs a file from top to bottom. Defining a class or function prepares it for later use; it does not immediately run its body. Indentation decides which instructions belong to which block. In app.py, most code runs later when a window event calls a method.

## measurement.py

### Line 1

```python
"""Measure an image-space vertical gap from two lip points and a hip point."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Measure an image-space vertical gap from two lip points and a hip point.

### Line 2

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 3

```python
import math
```

Load Python's maths library. This project uses isfinite to reject infinity and missing numeric values such as NaN.

### Line 4

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 5

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 6

```python
def measure_height(lip_a, lip_b, hip, pixels_per_metre=None):
```

Define the method or function measure_height. Its indented body runs when it is called. lip_a and lip_b are the two lip coordinate pairs. hip is the hip pair. pixels_per_metre defaults to None, so conversion is optional. The next line describes its job.

### Line 7

```python
    """Return signed original-image pixels and an optional rough metre estimate."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Return signed original-image pixels and an optional rough metre estimate.

### Line 8

```python
    x1, y1 = lip_a
```

Unpack the first lip point into its horizontal coordinate x1 and vertical coordinate y1. A point must contain two numeric values.

### Line 9

```python
    x2, y2 = lip_b
```

Unpack the second lip point into x2 and y2. The order of the two lip points may be reversed.

### Line 10

```python
    hip_x, hip_y = hip
```

Unpack the hip point into its x and y coordinates.

### Line 11

```python
    values = (x1, y1, x2, y2, hip_x, hip_y)
```

Gather all six coordinates in a tuple so they can be checked together.

### Line 12

```python
    if not all(math.isfinite(value) for value in values):
```

Check each coordinate with math.isfinite. all is true only if every check is true. not makes this condition true if any coordinate is NaN or infinity.

### Line 13

```python
        raise ValueError('All point coordinates must be finite numbers.')
```

Report a bad coordinate with ValueError. This prevents an invalid result from appearing as if it were a valid height.

### Line 14

```python
    if abs(x2 - x1) < 5:
```

Find the absolute horizontal separation of the lip points. Reject separations below five original pixels, because dividing by a tiny width is unstable and a vertical lip cannot be interpolated this way.

### Line 15

```python
        raise ValueError('Choose lip points at least 5 pixels apart horizontally.')
```

Report that the two lip points need a wider horizontal separation.

### Line 16

```python
    if not min(x1, x2) <= hip_x <= max(x1, x2):
```

Require the hip x position to be between the lip points' x positions, including the endpoints. min and max make this work with either click order.

### Line 17

```python
        raise ValueError('The two lip points must bracket the hip horizontally.')
```

Report a hip outside the chosen lip segment. The prototype deliberately avoids extending the line into an unmarked region.

### Line 18

```python
    lip_y = y1 + (y2 - y1) * (hip_x - x1) / (x2 - x1)
```

Interpolate the lip y position at hip_x. The lip's rise is y2-y1, its horizontal span is x2-x1, and the fraction travelled is (hip_x-x1)/(x2-x1). Add that fraction of the rise to y1. For a horizontal lip both y values are equal, so the rise is zero.

### Line 19

```python
    height_px = lip_y - hip_y
```

Subtract hip y from the lip y at the same x position. Image y increases downwards, so a higher hip gives a positive result. A lower hip gives a negative result.

### Line 20

```python
    height_m = None
```

Start with no metre estimate. None means unknown here rather than zero metres.

### Line 21

```python
    if pixels_per_metre is not None:
```

Only attempt metre conversion when the caller supplied a scale value.

### Line 22

```python
        if not math.isfinite(pixels_per_metre) or pixels_per_metre <= 0:
```

Reject scales that are NaN, infinite, zero, or negative. A valid pixels-per-metre scale must be a finite positive number.

### Line 23

```python
            raise ValueError('Pixels per metre must be a finite number above zero.')
```

Raise a readable bad-scale error when that condition fails.

### Line 24

```python
        height_m = height_px / pixels_per_metre
```

Divide the original pixel gap by the number of original pixels representing one metre. This is only a rough estimate when the scale assumptions are valid.

### Line 25

```python
    return height_px, height_m, lip_y
```

Return three values as a tuple: the signed pixel gap, optional metre estimate, and interpolated lip y. The app uses lip y to draw the vertical overlay.

## app.py

### Line 1

```python
"""Prototype-2: manually measure selected halfpipe jump frames."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Prototype-2: manually measure selected halfpipe jump frames.

### Line 2

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 3

```python
import csv
```

Load Python's CSV library. It writes dictionaries as rows in a comma-separated table file.

### Line 4

```python
import math
```

Load Python's maths library. This project uses isfinite to reject infinity and missing numeric values such as NaN.

### Line 5

```python
import sys
```

Load access to Python runtime information. Here it is used to read the optional video filename passed when starting the program.

### Line 6

```python
import tkinter as tk
```

Load the built-in window library and give it the shorter name tk. Later, tk.Tk creates a window and tk.Canvas creates a drawing area.

### Line 7

```python
from pathlib import Path
```

Import Path, a helper for file paths. Path(source).name gets just a filename instead of its whole folder path.

### Line 8

```python
from tkinter import filedialog, messagebox, simpledialog, ttk
```

Import file pickers, message popups, simple input popups, and themed window controls. ttk supplies buttons, labels, fields, and the results table.

### Line 9

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 10

```python
import cv2
```

Load OpenCV under its Python name cv2. It opens videos, reads frames, moves to frame numbers, and converts image colours.

### Line 11

```python
from PIL import Image, ImageTk
```

Import Pillow's image tools. Image handles an image; ImageTk converts it into a picture that Tkinter can display. Pillow keeps the older package name PIL.

### Line 12

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 13

```python
from measurement import measure_height
```

Import our own measurement function from measurement.py in this folder. This keeps the maths separate from the window code.

### Line 14

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 15

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 16

```python
class JumpApp:
```

Define a class named JumpApp. A class groups related values and methods. The app later creates one instance that remembers its current video and measurements.

### Line 17

```python
    """Keep the video, click positions, saved jumps, and window together."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Keep the video, click positions, saved jumps, and window together.

### Line 18

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 19

```python
    def __init__(self, root):
```

Define the method or function __init__. Its indented body runs when it is called. self is the new app instance and root is the window supplied by the caller. The next line describes its job.

### Line 20

```python
        self.root = root
```

Save the window passed into __init__ as self.root. Every method can now access the same window through self.

### Line 21

```python
        self.capture = None
```

Start without a video reader. None is a special value meaning that the reader does not exist yet.

### Line 22

```python
        self.frame = None
```

Start without an image. Later, a successful video read replaces None with an array of pixel colours.

### Line 23

```python
        self.source = ''
```

Start with an empty source string. A source will be a local filename or a direct video link.

### Line 24

```python
        self.frame_index = 0
```

Set the current frame number to 0. Video frame numbers in this app start at zero.

### Line 25

```python
        self.points = []
```

Store an empty list of click positions on this app. It has no lip or hip marks until the user clicks the image.

### Line 26

```python
        self.records = {}
```

Create an empty dictionary for saved measurements. Its key will combine the video source and jump label, so saving that pair again replaces its row.

### Line 27

```python
        self.root.title('Halfpipe | Prototype-2')
```

Set the text in the window title bar. The vertical bar is simply part of the title text.

### Line 28

```python
        self.root.resizable(False, False)
```

Disable manual resizing in both width and height. False means no. The preview and click conversion use a fixed canvas size.

### Line 29

```python
        toolbar = ttk.Frame(root, padding=8)
```

Create a container for the top row of buttons. root is its parent. padding=8 leaves space inside its edges.

### Line 30

```python
        toolbar.pack(fill='x')
```

Place the toolbar in the window and stretch it horizontally. pack is a Tkinter layout method; fill=x fills the available width.

### Line 31

```python
        ttk.Button(toolbar, text='Open video', command=self.open_file).pack(side='left')
```

Create and place the Open video button on the toolbar's left side. command=self.open_file passes the method itself, without calling it until the button is clicked.

### Line 32

```python
        ttk.Button(toolbar, text='Open link', command=self.open_link).pack(side='left')
```

Create the Open link button. Clicking it calls open_link later. pack(side=left) places it next to the previous button.

### Line 33

```python
        ttk.Button(toolbar, text='Reset points', command=self.reset_points).pack(side='left')
```

Create Reset points. Clicking it calls reset_points and removes the current image marks.

### Line 34

```python
        ttk.Button(toolbar, text='Export CSV', command=self.export_csv).pack(side='right')
```

Create Export CSV at the right side of the toolbar. Its command calls export_csv when clicked.

### Line 35

```python
        self.canvas = tk.Canvas(root, width=960, height=540, bg='#20252b', highlightthickness=0)
```

Create a 960 by 540 pixel drawing area. bg supplies a dark background colour. highlightthickness=0 removes the extra focus border around it.

### Line 36

```python
        self.canvas.pack()
```

Place the video canvas in the window below the toolbar.

### Line 37

```python
        self.canvas.bind('<Button-1>', self.click)
```

Register click as the handler for a left mouse button press in the canvas. Tkinter passes a mouse event with x and y coordinates to that method.

### Line 38

```python
        self.slider = tk.Scale(root, from_=0, to=0, orient='horizontal', length=940)
```

Create a horizontal slider for frame numbers. Its initial minimum and maximum are both 0. from_ has an underscore because from is a reserved Python word.

### Line 39

```python
        self.slider.pack()
```

Place the slider below the video canvas.

### Line 40

```python
        self.slider.bind('<ButtonRelease-1>', self.seek_slider)
```

Call seek_slider after the user releases the left mouse button on the slider. Waiting for release avoids decoding every frame during a drag.

### Line 41

```python
        self.slider.bind('<KeyRelease>', self.seek_slider)
```

Also call seek_slider when a key is released while the slider has focus. This allows keyboard changes to select frames.

### Line 42

```python
        controls = ttk.Frame(root, padding=8)
```

Create a second padded container, this time for navigation buttons and measurement fields.

### Line 43

```python
        controls.pack(fill='x')
```

Place this controls container below the slider and fill the window's width.

### Line 44

```python
        for label, step in [('-30 frames', -30), ('Previous', -1), ('Next', 1), ('+30 frames', 30)]:
```

Loop over four pairs. Each pair contains a button label and its frame offset. Negative offsets go backwards; positive offsets go forwards.

### Line 45

```python
            ttk.Button(controls, text=label, command=lambda n=step: self.show_frame(self.frame_index + n)).pack(side='left')
```

Create one navigation button for each pair. lambda makes a tiny function to run later. n=step remembers this button's offset, rather than letting all buttons use the loop's last value. It calls show_frame with the current frame plus that offset.

### Line 46

```python
        ttk.Label(controls, text='Jump label:').pack(side='left', padx=8)
```

Show the text Jump label beside the navigation buttons. padx=8 adds horizontal spacing around the label.

### Line 47

```python
        self.jump = tk.StringVar(value='1')
```

Create a Tkinter text variable starting with 1. Unlike an ordinary string, StringVar can stay connected to a text field.

### Line 48

```python
        ttk.Entry(controls, textvariable=self.jump, width=10).pack(side='left')
```

Create a short editable field linked to self.jump. Typing into it updates that variable. width=10 is approximately ten text characters.

### Line 49

```python
        ttk.Label(controls, text='Pixels/metre (optional):').pack(side='left', padx=8)
```

Show the label for the optional scale field. It tells the user that the number means original pixels per metre.

### Line 50

```python
        self.scale = tk.StringVar()
```

Create an initially empty text variable for the optional scale. Empty means no metre estimate should be calculated.

### Line 51

```python
        ttk.Entry(controls, textvariable=self.scale, width=10).pack(side='left')
```

Create a ten-character text field connected to self.scale. It accepts text; save_jump later tries to convert that text into a number.

### Line 52

```python
        ttk.Button(controls, text='Save/replace jump', command=self.save_jump).pack(side='right')
```

Place the save button at the controls row's right side. Clicking it calls save_jump to store or replace one result.

### Line 53

```python
        self.status = tk.StringVar(value='Open a video. Click lip A, lip B, then the centre of the hip.')
```

Create a status text variable containing the initial instructions. Updating this variable later also updates its visible label.

### Line 54

```python
        ttk.Label(root, textvariable=self.status, padding=8).pack(fill='x')
```

Show the status variable in a padded label below the controls. fill=x stretches the label across the window.

### Line 55

```python
        columns = ('video', 'jump', 'frame', 'seconds', 'height_px', 'height_m')
```

Define the six column names shown in the results table. This ordered tuple also controls how values are arranged when rows are inserted.

### Line 56

```python
        self.table = ttk.Treeview(root, columns=columns, show='headings', height=5)
```

Create the results table using those columns. show=headings hides the unused tree column. height=5 requests space for about five rows.

### Line 57

```python
        for column in columns:
```

Loop over each of the six column names so the next two lines can set its heading and width.

### Line 58

```python
            self.table.heading(column, text=column)
```

Set the current column's visible heading to its own name, such as height_px.

### Line 59

```python
            self.table.column(column, width=150)
```

Give that column a starting width of 150 screen pixels.

### Line 60

```python
        self.table.pack(fill='x', padx=8, pady=8)
```

Place the table below the status label with space around it. The table stores the displayed rows; self.records holds their underlying data.

### Line 61

```python
        self.root.protocol('WM_DELETE_WINDOW', self.close)
```

Tell Tkinter to call close when the window close button is pressed. WM_DELETE_WINDOW is the window manager's standard close event name.

### Line 62

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 63

```python
    def open_file(self):
```

Define the method or function open_file. Its indented body runs when it is called. self is the app instance. The next line describes its job.

### Line 64

```python
        """Ask for a local video and leave the current video alone if cancelled."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Ask for a local video and leave the current video alone if cancelled.

### Line 65

```python
        source = filedialog.askopenfilename(filetypes=[('Video', '*.mp4 *.mov *.avi *.mkv'), ('All files', '*.*')])
```

Open a file picker. filetypes offers common video extensions and an all-files option. The returned string is a path, or empty if cancelled.

### Line 66

```python
        if source:
```

Continue only if the dialog returned a nonempty string. Cancelling a dialog returns an empty or missing value, so nothing is loaded.

### Line 67

```python
            self.load_video(source)
```

Pass the selected path to load_video. That method checks the file and prepares its first frame.

### Line 68

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 69

```python
    def open_link(self):
```

Define the method or function open_link. Its indented body runs when it is called. self is the app instance. The next line describes its job.

### Line 70

```python
        """Ask for a direct HTTP video link, which may load slowly."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Ask for a direct HTTP video link, which may load slowly.

### Line 71

```python
        source = simpledialog.askstring('Open link', 'Paste a direct HTTPS or HTTP video link:')
```

Open a text input popup with a title and prompt. Its return value is the typed link, or None if cancelled.

### Line 72

```python
        if source:
```

Continue only if the dialog returned a nonempty string. Cancelling a dialog returns an empty or missing value, so nothing is loaded.

### Line 73

```python
            if source.strip().startswith(('https://', 'http://')):
```

Remove spaces from the start and end, then check for an HTTP or HTTPS prefix. startswith accepts a tuple so either prefix is allowed.

### Line 74

```python
                self.load_video(source.strip())
```

Pass the trimmed link to the shared video-loading method. It is treated as a video source rather than a webpage to browse.

### Line 75

```python
            else:
```

Run the next indented block only when the matching if condition was false.

### Line 76

```python
                messagebox.showerror('Invalid link', 'Use a direct HTTPS or HTTP video link.')
```

Show an error popup when the typed text lacks an accepted link prefix. This avoids trying unrelated text as a video location.

### Line 77

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 78

```python
    def load_video(self, source):
```

Define the method or function load_video. Its indented body runs when it is called. self is this app and source is a local video path or direct link. The next line describes its job.

### Line 79

```python
        """Check a new video before replacing the currently loaded one."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Check a new video before replacing the currently loaded one.

### Line 80

```python
        options = [cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 10000, cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000]
```

Build the OpenCV option list. Each property name is followed by its numeric value: 10000 milliseconds for opening and 5000 for reading. Those are 10 and 5 seconds.

### Line 81

```python
        capture = cv2.VideoCapture(source, cv2.CAP_FFMPEG, options)
```

Create a temporary video reader for the supplied source using the FFmpeg backend and timeout options. It is not yet the app's active reader.

### Line 82

```python
        ok, frame = capture.read()
```

Read the first frame from the temporary reader. ok says whether reading worked; frame contains the image if it did.

### Line 83

```python
        fps = capture.get(cv2.CAP_PROP_FPS)
```

Ask OpenCV for the video's reported frames per second. This is used for the approximate seconds column.

### Line 84

```python
        count = capture.get(cv2.CAP_PROP_FRAME_COUNT)
```

Ask OpenCV for the video's reported total frame count. The slider needs this to know its maximum.

### Line 85

```python
        if not ok or not math.isfinite(fps) or fps <= 0 or not math.isfinite(count) or count < 1:
```

Reject an unreadable first frame, a missing or nonpositive frame rate, or a missing or empty frame count. or means any one failure is enough; not reverses a yes/no condition.

### Line 86

```python
            capture.release()
```

Close the temporary reader after a failed check. The previously loaded video, if any, stays attached to the app.

### Line 87

```python
            messagebox.showerror('Cannot open video', 'Use a readable local clip with a frame count and frame rate.')
```

Explain the failed video check in a popup. The current version needs readable metadata and a decodable first frame.

### Line 88

```python
            return
```

End this method immediately without sending back a result. This prevents later instructions from running when a required condition was not met.

### Line 89

```python
        if self.capture is not None:
```

Check whether a video reader exists before trying to close it. is not None tests that this value is not the missing-value marker.

### Line 90

```python
            self.capture.release()
```

Close the video reader and release its resources. self.capture is the reader currently attached to this app.

### Line 91

```python
        self.capture = capture
```

Make the checked temporary reader the app's active reader. The previous reader was closed by the preceding condition.

### Line 92

```python
        self.source = source
```

Remember the exact source used to open the video. It identifies saved rows together with their jump labels.

### Line 93

```python
        self.fps = fps
```

Remember the reported frame rate on this app so save_jump can calculate seconds.

### Line 94

```python
        self.frame_count = int(count)
```

Convert the reported floating-point frame count into an integer and store it.

### Line 95

```python
        self.frame_index = 0
```

Set the current frame index back to the first frame of the newly loaded video.

### Line 96

```python
        self.frame = frame
```

Store the first decoded image as the current frame to display.

### Line 97

```python
        self.slider.configure(to=self.frame_count - 1)
```

Set the slider's maximum to the last valid frame number. Subtract one because counting starts at zero.

### Line 98

```python
        self.slider.set(0)
```

Move the slider to zero so it agrees with the first frame already read.

### Line 99

```python
        self.scale.set('')
```

Empty the pixels-per-metre field. A scale from a different frame or video may no longer be valid after the camera moves.

### Line 100

```python
        self.reset_points()
```

Call reset_points to clear the clicks, redraw the current frame, and show the marking instructions.

### Line 101

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 102

```python
    def seek_slider(self, event):
```

Define the method or function seek_slider. Its indented body runs when it is called. self is this app. event is the Tkinter mouse or keyboard event. This method does not need to inspect it. The next line describes its job.

### Line 103

```python
        """Read the slider after a mouse or keyboard movement."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Read the slider after a mouse or keyboard movement.

### Line 104

```python
        self.show_frame(self.slider.get())
```

Read the slider's current numeric value and ask show_frame to load that frame.

### Line 105

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 106

```python
    def show_frame(self, index):
```

Define the method or function show_frame. Its indented body runs when it is called. self is this app and index is the requested frame number. The next line describes its job.

### Line 107

```python
        """Seek to one frame and clear points that belong to the previous frame."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Seek to one frame and clear points that belong to the previous frame.

### Line 108

```python
        if self.capture is None:
```

Check whether the app still has no video reader. Navigation does nothing until a video is open.

### Line 109

```python
            return
```

End this method immediately without sending back a result. This prevents later instructions from running when a required condition was not met.

### Line 110

```python
        index = max(0, min(int(index), self.frame_count - 1))
```

Convert the requested index to an integer and clamp it between zero and the final frame. min enforces the upper bound; max enforces the lower bound.

### Line 111

```python
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, index)
```

Tell OpenCV which frame should be decoded next. CAP_PROP_POS_FRAMES is the next-frame index property.

### Line 112

```python
        ok, frame = self.capture.read()
```

Ask the current OpenCV reader for its next frame. Unpack the result into ok, a success flag, and frame, the image data.

### Line 113

```python
        if not ok:
```

Check whether the video reader failed to decode the requested frame.

### Line 114

```python
            self.slider.set(self.frame_index)
```

Move the slider back to the frame that is still displayed. A failed read should not leave it pointing to a different frame.

### Line 115

```python
            messagebox.showerror('Cannot read frame', 'Try another frame or a local clip.')
```

Show a readable failure message. A slow remote link or unsupported frame can cause reading to fail.

### Line 116

```python
            return
```

End this method immediately without sending back a result. This prevents later instructions from running when a required condition was not met.

### Line 117

```python
        self.frame_index = index
```

Remember the successfully requested frame number as the current index.

### Line 118

```python
        self.frame = frame
```

Replace the old displayed image data with the newly read frame.

### Line 119

```python
        self.slider.set(index)
```

Move the slider to the loaded index. This also keeps it in sync when a navigation button was used.

### Line 120

```python
        self.scale.set('')
```

Empty the pixels-per-metre field. A scale from a different frame or video may no longer be valid after the camera moves.

### Line 121

```python
        self.reset_points()
```

Call reset_points to clear the clicks, redraw the current frame, and show the marking instructions.

### Line 122

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 123

```python
    def reset_points(self):
```

Define the method or function reset_points. Its indented body runs when it is called. self is the app instance. The next line describes its job.

### Line 124

```python
        """Remove the current clicks without removing saved jumps."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Remove the current clicks without removing saved jumps.

### Line 125

```python
        self.points = []
```

Store an empty list of click positions on this app. It has no lip or hip marks until the user clicks the image.

### Line 126

```python
        self.draw()
```

Call the draw method now. It rebuilds the video image and the current point markers on the canvas.

### Line 127

```python
        self.status.set(f'Frame {self.frame_index}: click lip A, lip B, then hip. Recheck scale for this frame.')
```

Show instructions containing the current frame number. The f prefix lets the braces insert self.frame_index into the text.

### Line 128

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 129

```python
    def draw(self):
```

Define the method or function draw. Its indented body runs when it is called. self is the app instance. The next line describes its job.

### Line 130

```python
        """Fit the video inside the canvas without stretching its proportions."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Fit the video inside the canvas without stretching its proportions.

### Line 131

```python
        self.canvas.delete('all')
```

Remove every drawing item from the canvas before rebuilding it. This clears visual items only; it does not delete any file or saved record.

### Line 132

```python
        if self.frame is None:
```

Check whether there is no video image yet. The next return stops image work until a frame has been loaded.

### Line 133

```python
            return
```

End this method immediately without sending back a result. This prevents later instructions from running when a required condition was not met.

### Line 134

```python
        height, width = self.frame.shape[:2]
```

Read the image array's first two dimensions: height and width. [:2] means take the first two values. The remaining dimension describes colour channels.

### Line 135

```python
        self.display_scale = min(960 / width, 540 / height)
```

Choose the smaller of the width and height fitting ratios. Using one shared scale keeps the image's proportions while fitting inside 960 by 540.

### Line 136

```python
        image = Image.fromarray(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))
```

Convert OpenCV's blue-green-red colour order to red-green-blue, then turn the pixel array into a Pillow Image.

### Line 137

```python
        image = image.resize((round(width * self.display_scale), round(height * self.display_scale)))
```

Resize the Pillow image to the fitted width and height. round turns the computed dimensions into whole pixels.

### Line 138

```python
        self.photo = ImageTk.PhotoImage(image)
```

Convert the fitted image into a Tkinter picture. Saving it as self.photo keeps a Python reference alive; otherwise the picture can disappear.

### Line 139

```python
        self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
```

Draw the picture at the canvas origin. anchor=nw means its top left corner sits at x=0, y=0.

### Line 140

```python
        for index, (x, y) in enumerate(self.points):
```

Loop over the click positions, also getting their index with enumerate. Unpack each stored coordinate pair into x and y.

### Line 141

```python
            x, y = x * self.display_scale, y * self.display_scale
```

Multiply original-image coordinates by the display scale to find where those points appear in the smaller preview.

### Line 142

```python
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='yellow')
```

Draw a yellow circle around each displayed point. The four numbers define its bounding box, five pixels away on each side.

### Line 143

```python
            self.canvas.create_text(x + 12, y - 12, text=('Lip A', 'Lip B', 'Hip')[index], fill='yellow', anchor='w')
```

Choose Lip A, Lip B, or Hip by the point's index and draw the name near its marker. anchor=w aligns the text from its left edge.

### Line 144

```python
        if len(self.points) >= 2:
```

Draw a lip segment once at least two points exist. len counts how many click pairs are in the list.

### Line 145

```python
            coords = [value * self.display_scale for point in self.points[:2] for value in point]
```

Build a flat list of the first two points' scaled coordinates. The outer for chooses each point; the inner for chooses its x and y values.

### Line 146

```python
            self.canvas.create_line(*coords, fill='#00cfff', width=2)
```

Pass the four coordinate numbers separately with *coords and draw a blue line two pixels wide between the lip markers.

### Line 147

```python
        if len(self.points) == 3:
```

Run the measurement preview only after all three required points have been clicked.

### Line 148

```python
            try:
```

Start a block of instructions that might raise an error. The matching except block below handles the specified kind of error.

### Line 149

```python
                height_px, height_m, lip_y = measure_height(*self.points)
```

Expand the three points into the three position arguments for measure_height. Unpack its three returned values. No scale is passed here, so this preview only reports pixels.

### Line 150

```python
                x, y = self.points[2]
```

Get the third point, which is the hip. Index 2 is the third value because lists start at zero.

### Line 151

```python
                self.canvas.create_line(x * self.display_scale, y * self.display_scale, x * self.display_scale, lip_y * self.display_scale, fill='lime', width=2)
```

Draw a green vertical line from the hip to the interpolated lip. Multiply both endpoints by the display scale so the overlay matches the preview.

### Line 152

```python
                self.status.set(f'Image vertical gap: {height_px:.1f} px. Check points, then save the jump.')
```

Display the calculated pixel gap with one decimal place. The : .1f formatting, written without a space in the code, controls decimal precision.

### Line 153

```python
            except ValueError as error:
```

Handle a bad-value error from the try block. Store the error object in error so the app can show a readable explanation.

### Line 154

```python
                self.status.set(str(error))
```

Turn a caught measurement error into text and show it in the status label, so a bad point selection does not crash the app.

### Line 155

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 156

```python
    def click(self, event):
```

Define the method or function click. Its indented body runs when it is called. self is this app and event contains the mouse position inside the canvas. The next line describes its job.

### Line 157

```python
        """Convert a canvas click back into original video coordinates."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Convert a canvas click back into original video coordinates.

### Line 158

```python
        if self.frame is None or len(self.points) == 3:
```

Ignore clicks when there is no frame or when three points are already set. Reset points is required before making a different three-point selection.

### Line 159

```python
            return
```

End this method immediately without sending back a result. This prevents later instructions from running when a required condition was not met.

### Line 160

```python
        x, y = event.x / self.display_scale, event.y / self.display_scale
```

Convert the mouse position from preview pixels to original pixels by dividing by the fitting scale. The canvas image starts at its top left origin.

### Line 161

```python
        height, width = self.frame.shape[:2]
```

Read the image array's first two dimensions: height and width. [:2] means take the first two values. The remaining dimension describes colour channels.

### Line 162

```python
        if 0 <= x < width and 0 <= y < height:
```

Accept a click only inside the original image boundaries. Chained comparisons express both the lower and upper limit for each coordinate.

### Line 163

```python
            self.points.append((x, y))
```

Append the valid coordinate pair to the points list. The first two clicks represent the lip and the third represents the hip.

### Line 164

```python
            self.draw()
```

Call the draw method now. It rebuilds the video image and the current point markers on the canvas.

### Line 165

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 166

```python
    def save_jump(self):
```

Define the method or function save_jump. Its indented body runs when it is called. self is the app instance. The next line describes its job.

### Line 167

```python
        """Save one chosen peak frame per video and jump label."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Save one chosen peak frame per video and jump label.

### Line 168

```python
        if len(self.points) != 3:
```

Require exactly three points before saving. != means not equal.

### Line 169

```python
            messagebox.showerror('Missing points', 'Click lip A, lip B, and hip first.')
```

Show an error if one or more required clicks are missing.

### Line 170

```python
            return
```

End this method immediately without sending back a result. This prevents later instructions from running when a required condition was not met.

### Line 171

```python
        label = self.jump.get().strip()
```

Read the jump label field and trim surrounding spaces. The result becomes the label used in the record key and CSV.

### Line 172

```python
        if not label:
```

Reject an empty label so saved rows can be identified as individual jumps.

### Line 173

```python
            messagebox.showerror('Missing label', 'Enter a jump label, such as 1.')
```

Ask for a jump label in an error popup. It can be text or a number written as text.

### Line 174

```python
            return
```

End this method immediately without sending back a result. This prevents later instructions from running when a required condition was not met.

### Line 175

```python
        try:
```

Start a block of instructions that might raise an error. The matching except block below handles the specified kind of error.

### Line 176

```python
            scale = float(self.scale.get()) if self.scale.get().strip() else None
```

If the scale field has text after trimming, convert its contents to a decimal number with float. Otherwise use None. Invalid numeric text raises ValueError.

### Line 177

```python
            height_px, height_m, lip_y = measure_height(*self.points, pixels_per_metre=scale)
```

Calculate the pixel gap and optional metre estimate using the selected points and the supplied scale. pixels_per_metre=scale names that argument explicitly.

### Line 178

```python
        except ValueError as error:
```

Handle a bad-value error from the try block. Store the error object in error so the app can show a readable explanation.

### Line 179

```python
            messagebox.showerror('Check measurement', str(error))
```

Show the caught conversion or measurement error in a popup. The following return stops saving invalid results.

### Line 180

```python
            return
```

End this method immediately without sending back a result. This prevents later instructions from running when a required condition was not met.

### Line 181

```python
        row = dict(video=Path(self.source).name, jump=label, frame=self.frame_index, seconds=round(self.frame_index / self.fps, 3), height_px=round(height_px, 2), height_m='' if height_m is None else round(height_m, 3))
```

Build one dictionary for the result. Keep the source's filename, label, and frame. Divide frame by fps for seconds and round it to three decimals. Round pixels to two decimals. Store metres as an empty string if missing, or round to three decimals. Rounding changes displayed precision, not measurement accuracy.

### Line 182

```python
        row.update(pixels_per_metre='' if scale is None else scale)
```

Add the scale to the dictionary. Keep it blank when no scale was supplied, so the CSV does not confuse an unknown scale with zero.

### Line 183

```python
        for name, point in zip(('lip_a', 'lip_b', 'hip'), self.points):
```

Pair the three point names with their coordinate pairs using zip. Each loop iteration gives one name and one point.

### Line 184

```python
            row[name + '_x'], row[name + '_y'] = point
```

Split that point into x and y values stored under names such as lip_a_x and lip_a_y. Adding strings joins the name and suffix.

### Line 185

```python
        self.records[(self.source, label)] = row
```

Save the row under the tuple key of exact video source and jump label. Assigning an existing key replaces that row; a new key creates another row.

### Line 186

```python
        self.table.delete(*self.table.get_children())
```

Remove the currently displayed table rows before rebuilding the table. * expands all child row identifiers into separate arguments. self.records is kept.

### Line 187

```python
        for saved in self.records.values():
```

Loop over all saved dictionaries in their stored order. values gives the row values rather than the dictionary keys.

### Line 188

```python
            self.table.insert('', 'end', values=[saved[key] for key in self.table['columns']])
```

Insert one row at the end of the table. The empty parent identifier means a top-level row. The comprehension collects values in the table's column order.

### Line 189

```python
        self.status.set(f'Saved jump {label}. Choose a new label for the next jump. Export CSV before closing.')
```

Confirm which label was saved and remind the user to change labels for another jump and export before closing.

### Line 190

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 191

```python
    def export_csv(self):
```

Define the method or function export_csv. Its indented body runs when it is called. self is the app instance. The next line describes its job.

### Line 192

```python
        """Write all saved rows, including their clicked coordinates, to a CSV file."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Write all saved rows, including their clicked coordinates, to a CSV file.

### Line 193

```python
        if not self.records:
```

Check whether the saved-records dictionary is empty. An empty collection is false in an if condition.

### Line 194

```python
            messagebox.showinfo('No jumps', 'Save at least one jump first.')
```

Show an information popup when there are no measurements to export.

### Line 195

```python
            return
```

End this method immediately without sending back a result. This prevents later instructions from running when a required condition was not met.

### Line 196

```python
        path = filedialog.asksaveasfilename(defaultextension='.csv', initialfile='jumps.csv', filetypes=[('CSV', '*.csv')])
```

Open a save-file dialog with CSV as the file type and jumps.csv as the suggested name. A filename without an extension receives .csv.

### Line 197

```python
        if not path:
```

Check whether the save dialog was cancelled and returned an empty path.

### Line 198

```python
            return
```

End this method immediately without sending back a result. This prevents later instructions from running when a required condition was not met.

### Line 199

```python
        rows = list(self.records.values())
```

Make a list of all saved result dictionaries. This provides the rows and allows looking at the first row to obtain the column names.

### Line 200

```python
        try:
```

Start a block of instructions that might raise an error. The matching except block below handles the specified kind of error.

### Line 201

```python
            with open(path, 'w', newline='', encoding='utf-8-sig') as file:
```

Open the chosen path for writing inside a context manager. w creates or replaces the file. newline prevents extra blank lines in Windows CSV files. utf-8-sig adds a UTF-8 marker that helps Excel read text. with closes the file automatically.

### Line 202

```python
                writer = csv.DictWriter(file, fieldnames=list(rows[0]))
```

Create a CSV writer that uses dictionary keys as column names. list(rows[0]) gets the first row's keys in their insertion order.

### Line 203

```python
                writer.writeheader()
```

Write the column names as the first line of the CSV file.

### Line 204

```python
                writer.writerows(rows)
```

Write every result dictionary as one CSV row under those column names.

### Line 205

```python
            self.status.set(f'Exported {len(rows)} jumps to {Path(path).name}.')
```

Show the number of exported rows and the output filename. len counts rows; Path(path).name drops the folder part.

### Line 206

```python
        except OSError as error:
```

Handle a file-system error, such as a folder that cannot be written or a CSV locked by another program. Store it as error.

### Line 207

```python
            messagebox.showerror('Cannot export', str(error))
```

Show the export error message to the user instead of silently pretending the file was saved.

### Line 208

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 209

```python
    def close(self):
```

Define the method or function close. Its indented body runs when it is called. self is the app instance. The next line describes its job.

### Line 210

```python
        """Release the video reader when the user closes the window."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Release the video reader when the user closes the window.

### Line 211

```python
        if self.capture is not None:
```

Check whether a video reader exists before trying to close it. is not None tests that this value is not the missing-value marker.

### Line 212

```python
            self.capture.release()
```

Close the video reader and release its resources. self.capture is the reader currently attached to this app.

### Line 213

```python
        self.root.destroy()
```

Destroy the window and its controls. This ends the window event loop and loses any records that were not exported.

### Line 214

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 215

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 216

```python
if __name__ == '__main__':
```

Run the following block only when this file is started directly. Importing it from another file will define its functions and classes without starting its main program.

### Line 217

```python
    root = tk.Tk()
```

Create the main Tkinter window and name it root.

### Line 218

```python
    app = JumpApp(root)
```

Create a JumpApp instance attached to that window. Python automatically calls __init__, which builds the controls and initial state.

### Line 219

```python
    if len(sys.argv) > 1:
```

Check whether a video source was supplied after the script name on the command line. sys.argv includes the script itself as element 0.

### Line 220

```python
        app.load_video(sys.argv[1])
```

Load the first supplied argument as a video source. For example, app.py examples/demo.mp4 opens the included demo.

### Line 221

```python
    root.mainloop()
```

Start Tkinter's event loop. It waits for clicks, key presses, and window events, then calls the methods registered for those actions.

## test_measurement.py

### Line 1

```python
"""Small checks for the measurement formula and invalid inputs."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Small checks for the measurement formula and invalid inputs.

### Line 2

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 3

```python
import unittest
```

Load Python's built-in test library. It runs named checks and reports whether each one passed or failed.

### Line 4

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 5

```python
from measurement import measure_height
```

Import our own measurement function from measurement.py in this folder. This keeps the maths separate from the window code.

### Line 6

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 7

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 8

```python
class MeasurementTests(unittest.TestCase):
```

Define a test class that inherits assertion tools from unittest.TestCase. Methods whose names begin with test_ are discovered as individual tests.

### Line 9

```python
    """Check cases that could otherwise produce a misleading measurement."""
```

A docstring, written as a triple-quoted string. It documents this file, class, or method: Check cases that could otherwise produce a misleading measurement.

### Line 10

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 11

```python
    def test_horizontal_lip(self):
```

Define the method or function test_horizontal_lip. Its indented body runs when it is called. self is this test case, with assertion helpers supplied by unittest. The next line describes its job.

### Line 12

```python
        result = measure_height((100, 400), (800, 400), (450, 160), 80)
```

Measure a horizontal lip at y=400 and a hip at y=160 with a scale of 80 pixels per metre. The expected gap is 240 pixels and the estimate is 3 metres.

### Line 13

```python
        self.assertEqual(result, (240, 3, 400))
```

Check all three returned values: 240 pixels, 3 metres, and lip y=400. Equal whole and decimal numeric values compare equal in Python.

### Line 14

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 15

```python
    def test_sloped_lip(self):
```

Define the method or function test_sloped_lip. Its indented body runs when it is called. self is this test case, with assertion helpers supplied by unittest. The next line describes its job.

### Line 16

```python
        result = measure_height((100, 300), (500, 500), (300, 250))
```

Measure a sloped lip from (100,300) to (500,500). At hip x=300 its y must be 400. The hip is at y=250, so the gap must be 150 pixels.

### Line 17

```python
        self.assertEqual(result, (150, None, 400))
```

Compare the whole returned tuple with the expected values: a 150 pixel gap, no metre estimate, and lip y=400. Any mismatch fails the test.

### Line 18

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 19

```python
    def test_reversed_lip_points(self):
```

Define the method or function test_reversed_lip_points. Its indented body runs when it is called. self is this test case, with assertion helpers supplied by unittest. The next line describes its job.

### Line 20

```python
        result = measure_height((500, 500), (100, 300), (300, 250))
```

Use the same sloped lip as before but reverse its two endpoints. The formula should still produce the same result.

### Line 21

```python
        self.assertEqual(result, (150, None, 400))
```

Compare the whole returned tuple with the expected values: a 150 pixel gap, no metre estimate, and lip y=400. Any mismatch fails the test.

### Line 22

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 23

```python
    def test_below_lip_is_negative(self):
```

Define the method or function test_below_lip_is_negative. Its indented body runs when it is called. self is this test case, with assertion helpers supplied by unittest. The next line describes its job.

### Line 24

```python
        result = measure_height((100, 400), (800, 400), (450, 450))
```

Put the hip at y=450 while the horizontal lip is at y=400. The expected signed gap is 400-450=-50 pixels.

### Line 25

```python
        self.assertEqual(result[0], -50)
```

Check that the first returned value, the pixel gap, is -50. A hip below the lip must keep a negative sign.

### Line 26

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 27

```python
    def test_on_lip_is_zero(self):
```

Define the method or function test_on_lip_is_zero. Its indented body runs when it is called. self is this test case, with assertion helpers supplied by unittest. The next line describes its job.

### Line 28

```python
        result = measure_height((100, 400), (800, 400), (450, 400))
```

Put the hip directly on the horizontal lip. Its gap should be zero.

### Line 29

```python
        self.assertEqual(result[0], 0)
```

Check that the first returned value is exactly zero when the hip lies on the lip.

### Line 30

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 31

```python
    def test_nearly_vertical_lip_is_rejected(self):
```

Define the method or function test_nearly_vertical_lip_is_rejected. Its indented body runs when it is called. self is this test case, with assertion helpers supplied by unittest. The next line describes its job.

### Line 32

```python
        with self.assertRaises(ValueError):
```

Expect the indented call to raise ValueError. The test fails if no such error is raised, so invalid input cannot silently produce a result.

### Line 33

```python
            measure_height((100, 400), (102, 500), (101, 200))
```

Try lip endpoints separated by only two horizontal pixels. This must raise ValueError instead of producing an unstable result.

### Line 34

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 35

```python
    def test_hip_outside_segment_is_rejected(self):
```

Define the method or function test_hip_outside_segment_is_rejected. Its indented body runs when it is called. self is this test case, with assertion helpers supplied by unittest. The next line describes its job.

### Line 36

```python
        with self.assertRaises(ValueError):
```

Expect the indented call to raise ValueError. The test fails if no such error is raised, so invalid input cannot silently produce a result.

### Line 37

```python
            measure_height((100, 400), (800, 400), (900, 160))
```

Place the hip at x=900, outside lip endpoints x=100 and x=800. This must be rejected.

### Line 38

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 39

```python
    def test_invalid_scales_are_rejected(self):
```

Define the method or function test_invalid_scales_are_rejected. Its indented body runs when it is called. self is this test case, with assertion helpers supplied by unittest. The next line describes its job.

### Line 40

```python
        for scale in (0, -1, float('nan'), float('inf')):
```

Repeat the invalid-scale test for zero, a negative number, NaN, and positive infinity. float creates the two special numeric values from text.

### Line 41

```python
            with self.subTest(scale=scale):
```

Name each repeated test case by its scale. subTest makes it easier to see which input failed while still checking all four.

### Line 42

```python
                with self.assertRaises(ValueError):
```

Expect the indented call to raise ValueError. The test fails if no such error is raised, so invalid input cannot silently produce a result.

### Line 43

```python
                    measure_height((100, 400), (800, 400), (450, 160), scale)
```

Call measure_height with the current invalid scale. The surrounding assertRaises block requires it to raise ValueError.

### Line 44

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 45

```python
    def test_nonfinite_point_is_rejected(self):
```

Define the method or function test_nonfinite_point_is_rejected. Its indented body runs when it is called. self is this test case, with assertion helpers supplied by unittest. The next line describes its job.

### Line 46

```python
        with self.assertRaises(ValueError):
```

Expect the indented call to raise ValueError. The test fails if no such error is raised, so invalid input cannot silently produce a result.

### Line 47

```python
            measure_height((100, 400), (800, 400), (float('nan'), 160))
```

Try a hip x coordinate that is NaN. The measurement function must reject it before doing geometry.

### Line 48

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 49

```python

```

Blank line. It separates related parts for readability and performs no action.

### Line 50

```python
if __name__ == '__main__':
```

Run the following block only when this file is started directly. Importing it from another file will define its functions and classes without starting its main program.

### Line 51

```python
    unittest.main()
```

Find and run the tests in this file when it is started directly. Print their results and return a failure exit status if a check fails.

