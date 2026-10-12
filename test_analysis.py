"""Check detection geometry, jump grouping, and saved video sessions."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import cv2
import numpy as np

from analysis import analyse, export_csv, find_jumps
from vision import choose_athlete, find_lip


def person(x=160, y=100):
    return dict(box=[x - 20, y - 30, 40, 60], hip=[x, y], score=0.9, hip_score=0.9, points=[[0, 0, 0] for _ in range(17)], ambiguous=False)


def sample(second, gap, cut=False):
    return dict(time=second, frame=round(second * 10), height_px=gap, person=person(), lip=dict(extrapolated=False), confidence=0.8, cut=cut)


class JumpTests(unittest.TestCase):
    def test_missing_evidence_does_not_become_zero(self):
        samples = [sample(0, None), sample(1, -10), sample(2, 20)]
        self.assertEqual(find_jumps(samples, 10), [])

    def test_brief_gap_is_bridged_and_long_gap_splits(self):
        samples = [sample(0, 20), sample(0.1, 30), sample(0.2, None), sample(0.3, 25), sample(1, 20), sample(1.1, 30)]
        jumps = find_jumps(samples, 10)
        self.assertEqual(len(jumps), 2)
        self.assertEqual(jumps[0]['end'], 0.3)
        self.assertIsNone(jumps[0]['height_m'])
        self.assertFalse(jumps[0]['reviewed'])

    def test_camera_cut_splits_adjacent_candidates(self):
        samples = [sample(0, 20), sample(0.1, 30), sample(0.2, 40, True), sample(0.3, 35)]
        self.assertEqual(len(find_jumps(samples, 10)), 2)

    def test_single_spike_is_not_selected_as_peak(self):
        samples = [sample(i / 10, gap) for i, gap in enumerate([20, 30, 500, 40, 20])]
        self.assertEqual(find_jumps(samples, 10)[0]['height_px'], 40)

    def test_missing_person_cannot_be_a_jump(self):
        item = sample(0, 20)
        item['person'] = None
        self.assertEqual(find_jumps([item], 6), [])


class VisionTests(unittest.TestCase):
    def test_lip_fit_tracks_a_sloping_blue_boundary(self):
        frame = np.full((240, 320, 3), 245, dtype=np.uint8)
        cv2.line(frame, (20, 140), (300, 196), (255, 180, 30), 8)
        lip = find_lip(frame, [160, 80], [140, 50, 40, 60])
        self.assertIsNotNone(lip)
        self.assertAlmostEqual(lip['y'], 164, delta=5)

    def test_white_frame_has_no_lip(self):
        self.assertIsNone(find_lip(np.full((240, 320, 3), 255, dtype=np.uint8), [160, 80], [140, 50, 40, 60]))

    def test_continuity_prefers_the_previous_athlete(self):
        athlete, other = person(145), person(290)
        self.assertEqual(choose_athlete([other, athlete], (240, 320, 3), person(140))['hip'], athlete['hip'])

    def test_motion_can_release_a_stationary_spectator(self):
        spectator, athlete = person(145), person(170)
        spectator.update(score=0.95, motion=0)
        athlete.update(score=0.65, motion=0.9)
        self.assertEqual(choose_athlete([spectator, athlete], (240, 320, 3), spectator)['hip'], athlete['hip'])


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.folder = Path(self.temporary.name)
        self.video = self.folder / 'input.mp4'
        writer = cv2.VideoWriter(str(self.video), cv2.VideoWriter_fourcc(*'mp4v'), 10, (320, 240))
        self.assertTrue(writer.isOpened())
        for index in range(30):
            frame = np.full((240, 320, 3), 245, dtype=np.uint8)
            cv2.line(frame, (20, 160), (300, 160), (255, 180, 30), 8)
            writer.write(frame)
        writer.release()

    def tearDown(self):
        self.temporary.cleanup()

    def run_session(self, **settings):
        with patch('analysis.PoseDetector') as detector:
            detector.return_value.detect.return_value = [person()]
            return analyse(str(self.video), model_path='unused-in-this-mocked-test', folder=self.folder / 'session', sample_rate=5, **settings)

    def test_range_export_and_review_video(self):
        report = self.run_session(start=1, end=2)
        self.assertTrue(report['complete'])
        self.assertEqual(len(report['samples']), 5)
        self.assertEqual(report['samples'][0]['frame'], 10)
        self.assertLess(report['samples'][-1]['time'], 2)
        loaded = json.loads((self.folder / 'session/report.json').read_text())
        self.assertEqual(loaded['state'], 'complete')
        self.assertTrue((self.folder / 'session/jumps.csv').exists())
        capture = cv2.VideoCapture(str(self.folder / 'session/review.mp4'))
        self.assertTrue(capture.isOpened())
        self.assertEqual(int(capture.get(cv2.CAP_PROP_FRAME_COUNT)), 5)
        capture.release()
        report['jumps'][0].update(excluded=True, reviewed=True)
        export_csv(report, self.folder / 'export.csv')
        self.assertIn('True,True', (self.folder / 'export.csv').read_text(encoding='utf-8-sig'))

    def test_stop_preserves_partial_results(self):
        updates = []
        report = self.run_session(progress=updates.append, cancelled=lambda: len(updates) >= 2)
        self.assertEqual(report['state'], 'stopped')
        self.assertFalse(report['complete'])
        self.assertGreater(len(report['samples']), 0)
        self.assertLess(len(report['samples']), 15)
        self.assertTrue((self.folder / 'session/report.json').exists())

    def test_invalid_range_is_rejected(self):
        with self.assertRaises(ValueError):
            self.run_session(start=2, end=1)


if __name__ == '__main__':
    unittest.main()
