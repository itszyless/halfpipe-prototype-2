"""Verify the metre conversion and local vertical reference geometry."""

import unittest

from measurement import calibrate_height


class CalibrationTests(unittest.TestCase):
    def test_known_vertical_reference(self):
        metres, scale, gap = calibrate_height((0, 150), (300, 150), (150, 90), (100, 80), (100, 100), 1)
        self.assertEqual(metres, 3)
        self.assertEqual(scale, 20)
        self.assertEqual(gap, 60)

    def test_tilted_reference_uses_projected_vertical(self):
        metres, scale, gap = calibrate_height((0, 150), (300, 150), (100, 100), (100, 100), (130, 140), 2)
        self.assertAlmostEqual(gap, 62.5)
        self.assertEqual(scale, 25)
        self.assertAlmostEqual(metres, 2.5)

    def test_reference_order_and_short_length_are_rejected(self):
        for top, bottom in [((0, 20), (0, 0)), ((0, 0), (0, 5))]:
            with self.assertRaises(ValueError):
                calibrate_height((0, 100), (200, 100), (100, 50), top, bottom, 1)

    def test_parallel_reference_is_rejected(self):
        with self.assertRaises(ValueError):
            calibrate_height((0, 100), (200, 120), (100, 50), (0, 0), (100, 10), 1)

    def test_unknown_length_is_rejected(self):
        for length in [0, -1, float('nan')]:
            with self.assertRaises(ValueError):
                calibrate_height((0, 100), (200, 100), (100, 50), (0, 0), (0, 20), length)


if __name__ == '__main__':
    unittest.main()
