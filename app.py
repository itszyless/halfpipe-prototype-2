"""Prototype-2: manually measure selected halfpipe jump frames."""

import csv
import math
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

import cv2
from PIL import Image, ImageTk

from measurement import measure_height


class JumpApp:
    """Keep the video, click positions, saved jumps, and window together."""

    def __init__(self, root):
        self.root = root
        self.capture = None
        self.frame = None
        self.source = ''
        self.frame_index = 0
        self.points = []
        self.records = {}
        self.root.title('Halfpipe | Prototype-2')
        self.root.resizable(False, False)
        toolbar = ttk.Frame(root, padding=8)
        toolbar.pack(fill='x')
        ttk.Button(toolbar, text='Open video', command=self.open_file).pack(side='left')
        ttk.Button(toolbar, text='Open link', command=self.open_link).pack(side='left')
        ttk.Button(toolbar, text='Reset points', command=self.reset_points).pack(side='left')
        ttk.Button(toolbar, text='Export CSV', command=self.export_csv).pack(side='right')
        self.canvas = tk.Canvas(root, width=960, height=540, bg='#20252b', highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.click)
        self.slider = tk.Scale(root, from_=0, to=0, orient='horizontal', length=940)
        self.slider.pack()
        self.slider.bind('<ButtonRelease-1>', self.seek_slider)
        self.slider.bind('<KeyRelease>', self.seek_slider)
        controls = ttk.Frame(root, padding=8)
        controls.pack(fill='x')
        for label, step in [('-30 frames', -30), ('Previous', -1), ('Next', 1), ('+30 frames', 30)]:
            ttk.Button(controls, text=label, command=lambda n=step: self.show_frame(self.frame_index + n)).pack(side='left')
        ttk.Label(controls, text='Jump label:').pack(side='left', padx=8)
        self.jump = tk.StringVar(value='1')
        ttk.Entry(controls, textvariable=self.jump, width=10).pack(side='left')
        ttk.Label(controls, text='Pixels/metre (optional):').pack(side='left', padx=8)
        self.scale = tk.StringVar()
        ttk.Entry(controls, textvariable=self.scale, width=10).pack(side='left')
        ttk.Button(controls, text='Save/replace jump', command=self.save_jump).pack(side='right')
        self.status = tk.StringVar(value='Open a video. Click lip A, lip B, then the centre of the hip.')
        ttk.Label(root, textvariable=self.status, padding=8).pack(fill='x')
        columns = ('video', 'jump', 'frame', 'seconds', 'height_px', 'height_m')
        self.table = ttk.Treeview(root, columns=columns, show='headings', height=5)
        for column in columns:
            self.table.heading(column, text=column)
            self.table.column(column, width=150)
        self.table.pack(fill='x', padx=8, pady=8)
        self.root.protocol('WM_DELETE_WINDOW', self.close)

    def open_file(self):
        """Ask for a local video and leave the current video alone if cancelled."""
        source = filedialog.askopenfilename(filetypes=[('Video', '*.mp4 *.mov *.avi *.mkv'), ('All files', '*.*')])
        if source:
            self.load_video(source)

    def open_link(self):
        """Ask for a direct HTTP video link, which may load slowly."""
        source = simpledialog.askstring('Open link', 'Paste a direct HTTPS or HTTP video link:')
        if source:
            if source.strip().startswith(('https://', 'http://')):
                self.load_video(source.strip())
            else:
                messagebox.showerror('Invalid link', 'Use a direct HTTPS or HTTP video link.')

    def load_video(self, source):
        """Check a new video before replacing the currently loaded one."""
        options = [cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 10000, cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000]
        capture = cv2.VideoCapture(source, cv2.CAP_FFMPEG, options)
        ok, frame = capture.read()
        fps = capture.get(cv2.CAP_PROP_FPS)
        count = capture.get(cv2.CAP_PROP_FRAME_COUNT)
        if not ok or not math.isfinite(fps) or fps <= 0 or not math.isfinite(count) or count < 1:
            capture.release()
            messagebox.showerror('Cannot open video', 'Use a readable local clip with a frame count and frame rate.')
            return
        if self.capture is not None:
            self.capture.release()
        self.capture = capture
        self.source = source
        self.fps = fps
        self.frame_count = int(count)
        self.frame_index = 0
        self.frame = frame
        self.slider.configure(to=self.frame_count - 1)
        self.slider.set(0)
        self.scale.set('')
        self.reset_points()

    def seek_slider(self, event):
        """Read the slider after a mouse or keyboard movement."""
        self.show_frame(self.slider.get())

    def show_frame(self, index):
        """Seek to one frame and clear points that belong to the previous frame."""
        if self.capture is None:
            return
        index = max(0, min(int(index), self.frame_count - 1))
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, index)
        ok, frame = self.capture.read()
        if not ok:
            self.slider.set(self.frame_index)
            messagebox.showerror('Cannot read frame', 'Try another frame or a local clip.')
            return
        self.frame_index = index
        self.frame = frame
        self.slider.set(index)
        self.scale.set('')
        self.reset_points()

    def reset_points(self):
        """Remove the current clicks without removing saved jumps."""
        self.points = []
        self.draw()
        self.status.set(f'Frame {self.frame_index}: click lip A, lip B, then hip. Recheck scale for this frame.')

    def draw(self):
        """Fit the video inside the canvas without stretching its proportions."""
        self.canvas.delete('all')
        if self.frame is None:
            return
        height, width = self.frame.shape[:2]
        self.display_scale = min(960 / width, 540 / height)
        image = Image.fromarray(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))
        image = image.resize((round(width * self.display_scale), round(height * self.display_scale)))
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
        for index, (x, y) in enumerate(self.points):
            x, y = x * self.display_scale, y * self.display_scale
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='yellow')
            self.canvas.create_text(x + 12, y - 12, text=('Lip A', 'Lip B', 'Hip')[index], fill='yellow', anchor='w')
        if len(self.points) >= 2:
            coords = [value * self.display_scale for point in self.points[:2] for value in point]
            self.canvas.create_line(*coords, fill='#00cfff', width=2)
        if len(self.points) == 3:
            try:
                height_px, height_m, lip_y = measure_height(*self.points)
                x, y = self.points[2]
                self.canvas.create_line(x * self.display_scale, y * self.display_scale, x * self.display_scale, lip_y * self.display_scale, fill='lime', width=2)
                self.status.set(f'Image vertical gap: {height_px:.1f} px. Check points, then save the jump.')
            except ValueError as error:
                self.status.set(str(error))

    def click(self, event):
        """Convert a canvas click back into original video coordinates."""
        if self.frame is None or len(self.points) == 3:
            return
        x, y = event.x / self.display_scale, event.y / self.display_scale
        height, width = self.frame.shape[:2]
        if 0 <= x < width and 0 <= y < height:
            self.points.append((x, y))
            self.draw()

    def save_jump(self):
        """Save one chosen peak frame per video and jump label."""
        if len(self.points) != 3:
            messagebox.showerror('Missing points', 'Click lip A, lip B, and hip first.')
            return
        label = self.jump.get().strip()
        if not label:
            messagebox.showerror('Missing label', 'Enter a jump label, such as 1.')
            return
        try:
            scale = float(self.scale.get()) if self.scale.get().strip() else None
            height_px, height_m, lip_y = measure_height(*self.points, pixels_per_metre=scale)
        except ValueError as error:
            messagebox.showerror('Check measurement', str(error))
            return
        row = dict(video=Path(self.source).name, jump=label, frame=self.frame_index, seconds=round(self.frame_index / self.fps, 3), height_px=round(height_px, 2), height_m='' if height_m is None else round(height_m, 3))
        row.update(pixels_per_metre='' if scale is None else scale)
        for name, point in zip(('lip_a', 'lip_b', 'hip'), self.points):
            row[name + '_x'], row[name + '_y'] = point
        self.records[(self.source, label)] = row
        self.table.delete(*self.table.get_children())
        for saved in self.records.values():
            self.table.insert('', 'end', values=[saved[key] for key in self.table['columns']])
        self.status.set(f'Saved jump {label}. Choose a new label for the next jump. Export CSV before closing.')

    def export_csv(self):
        """Write all saved rows, including their clicked coordinates, to a CSV file."""
        if not self.records:
            messagebox.showinfo('No jumps', 'Save at least one jump first.')
            return
        path = filedialog.asksaveasfilename(defaultextension='.csv', initialfile='jumps.csv', filetypes=[('CSV', '*.csv')])
        if not path:
            return
        rows = list(self.records.values())
        try:
            with open(path, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.DictWriter(file, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            self.status.set(f'Exported {len(rows)} jumps to {Path(path).name}.')
        except OSError as error:
            messagebox.showerror('Cannot export', str(error))

    def close(self):
        """Release the video reader when the user closes the window."""
        if self.capture is not None:
            self.capture.release()
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = JumpApp(root)
    if len(sys.argv) > 1:
        app.load_video(sys.argv[1])
    root.mainloop()
