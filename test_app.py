"""Test native review actions without needing an interactive display."""

import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from PySide6.QtWidgets import QApplication

from app import MainWindow
from test_analysis import person, sample


class ReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.application = QApplication.instance() or QApplication([])

    def test_review_exclusion_scale_and_point_correction(self):
        with tempfile.TemporaryDirectory() as temporary, patch.object(MainWindow, 'load_recent'), patch.object(MainWindow, 'save_recent'):
            window = MainWindow()
            peak = sample(1, 60)
            peak['lip'].update(a=[20, 160], b=[300, 160], y=160)
            jump = dict(id=1, start=0.8, end=1.2, peak_time=1, frame=10, height_px=60, height_m=None, scale=None, confidence=0.8, reviewed=False, excluded=False, reasons=[], sample_index=0)
            report = dict(version=2, source='test.mp4', folder=temporary, start=0, end=3, fps=10, samples=[peak], jumps=[jump], state='complete', complete=True)
            window.receive_report(report)
            window.mark_reviewed()
            self.assertTrue(jump['reviewed'])
            window.exclude()
            self.assertTrue(jump['excluded'])
            window.correction_jump = jump
            window.reference_length.setValue(1)
            window.save_calibration([(160, 100), (160, 120)])
            self.assertEqual(jump['height_m'], 3)
            window.correction_jump = jump
            window.raw_frame = np.full((240, 320, 3), 255, dtype=np.uint8)
            window.correct_points([(20, 150), (300, 150), (160, 100)])
            self.assertEqual(jump['height_px'], 50)
            self.assertIsNone(jump['height_m'])
            self.assertTrue((Path(temporary) / jump['snapshot']).exists())
            window.pending_manual = dict(time=2, frame=20)
            window.correct_points([(20, 150), (300, 150), (160, 90)])
            self.assertEqual(len(report['jumps']), 2)
            self.assertTrue(report['jumps'][-1]['manual'])
            self.assertEqual(report['jumps'][-1]['height_px'], 60)
            window.resize(1100, 800)
            window.show()
            self.application.processEvents()
            self.assertGreater(window.canvas.width(), 400)
            window.close()


if __name__ == '__main__':
    unittest.main()
