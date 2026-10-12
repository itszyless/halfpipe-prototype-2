# Start here

Read this first, then open LINE_BY_LINE.md with the Python files next to it. You do not need to understand everything at once.

## What Python does

Python reads your instructions and runs them. A `.py` file is a text file containing those instructions. An error message tells you where Python could not continue. The last line of the error usually describes the problem.

An `import` gives your code access to another file or a library. A library is a collection of code you can reuse. Tkinter comes with a normal Python installation. OpenCV and Pillow are installed from requirements.txt. A virtual environment, called `.venv` here, keeps this project's installed libraries separate from other projects.

## Small pieces of the language

```python
height = 240
```

This creates a variable named `height` and gives it the value 240. A variable is a name for a value. `=` assigns a value. `==` checks whether two values are equal.

```python
name = 'jump 1'
points = [(200, 400), (760, 400), (480, 160)]
```

Text in quotes is a string. Square brackets make a list. A list keeps values in order and can change. Each `(x, y)` here is a tuple, a fixed pair of values. A dictionary uses keys to find values, such as `{'height_px': 240}`. `None` means a value is missing. `True` and `False` are yes and no values.

```python
if height > 0:
    print('Above the line')
```

`if` runs its indented instructions only when its condition is true. The colon starts the block. Spaces at the start of the next line show which block it belongs to. Python uses indentation instead of curly braces for blocks. `print` writes text to the terminal.

```python
def double(number):
    return number * 2
```

`def` defines a function, a reusable named piece of work. `number` is an input, called a parameter. `return` sends a result back and ends that function call. `double(3)` calls the function and produces 6. A function name without `()` can be passed to a button so the button calls it later.

```python
for point in points:
    print(point)
```

`for` repeats the indented work once for each value. `len(points)` counts the values. `points[0]` gets the first value because Python starts counting at 0. `points[:2]` gets the first two values. `x, y = point` splits a pair into two names.

`class JumpApp` groups related data and functions. `app = JumpApp(root)` creates one instance of that class. Its `__init__` method runs when it is created. `self` means that particular app instance. `self.points` is its list of clicks. A method is a function attached to an object. A dot accesses something attached to a module or object, such as `self.draw` or `math.isfinite`.

`try` starts work that might fail. `except ValueError as error` handles a bad-value error and gives it the name `error`. `raise ValueError(...)` reports that a value is not acceptable. `with open(...) as file` opens a file and closes it when the block ends, including when an error occurs.

`f'Height: {height:.1f}'` is formatted text. Python replaces the braces with a value. `.1f` displays one digit after the decimal point. A list comprehension, such as `[x * 2 for x in numbers]`, builds a list by repeating a calculation. `*points` in a function call expands a list into separate arguments.

Triple quotes contain a longer string. At the start of a file, class, or function, it is a docstring. It explains that piece of code. Empty lines separate ideas and do not run any instruction.

## Follow one measurement

1. `root = tk.Tk()` creates the window.
2. `JumpApp(root)` creates the buttons, video area, slider, fields, and table.
3. `root.mainloop()` waits for actions such as clicks. This is the event loop.
4. Open video calls `open_file`, which calls `load_video`.
5. OpenCV reads the first frame as a grid of colour values.
6. `draw` changes the colour order, fits the image into the window, and shows it.
7. Moving the slider calls `show_frame`. Old points and the old scale are cleared.
8. Each video click calls `click`. Its position is converted into original video pixels.
9. With three clicks, `measure_height` calculates the lip's y position at the hip's x position, then subtracts the hip's y position.
10. Save/replace jump builds a dictionary with that result and its coordinates.
11. Export CSV writes those dictionaries to a table file. CSV means comma-separated values. Excel can open it. Some local Excel settings require importing it with comma as the delimiter.

## Explain the maths in your own words

The first two clicks tell the app where the lip is in that frame. If the lip slopes, the app calculates where that line crosses the hip's horizontal position. It compares the two y positions. Because y increases downwards, lip y minus hip y is positive when the hip is above the lip.

For the demo, the lip is at y=400 and the hip is at y=160. The difference is 240 pixels. With the example scale of 80 pixels per metre, that is 3 metres. Without a known scale, 240 pixels alone cannot tell you the real height.

## What to tell the group

The current version is a manual baseline. It stores the chosen peak frame, clicked points, image gap, and optional scale. Its purpose is to make the measurement rule easy to test before adding tracking. Its main unsolved problem is converting a moving camera view into a reliable real-world height.

Ask the group for a short clip, trusted reference heights, camera calibration or event geometry, and the expected accuracy. You can already use the prototype without these, but leave metre estimates blank until a scale is justified.

## Safe first edits

Try changing a button's `text` value, running the app, and checking the result. Then change a status message. Read measurement.py and run the tests before changing the formula. Keep changes on the `prototype-2` branch.

If you see `ModuleNotFoundError`, run the install command with the same `.venv` Python used to start the app. If Tkinter is missing, use the standard Python installer with Tcl/Tk. If a video does not open, try the demo first, then a short local MP4. If the file is open in Excel and cannot be exported, close it or choose another filename.
