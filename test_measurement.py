"""Small checks for the measurement formula and invalid inputs."""

import unittest

from measurement import measure_height


class MeasurementTests(unittest.TestCase):
    """Check cases that could otherwise produce a misleading measurement."""

    def test_horizontal_lip(self):
        result = measure_height((100, 400), (800, 400), (450, 160), 80)
        self.assertEqual(result, (240, 3, 400))

    def test_sloped_lip(self):
        result = measure_height((100, 300), (500, 500), (300, 250))
        self.assertEqual(result, (150, None, 400))

    def test_reversed_lip_points(self):
        result = measure_height((500, 500), (100, 300), (300, 250))
        self.assertEqual(result, (150, None, 400))

    def test_below_lip_is_negative(self):
        result = measure_height((100, 400), (800, 400), (450, 450))
        self.assertEqual(result[0], -50)

    def test_on_lip_is_zero(self):
        result = measure_height((100, 400), (800, 400), (450, 400))
        self.assertEqual(result[0], 0)

    def test_nearly_vertical_lip_is_rejected(self):
        with self.assertRaises(ValueError):
            measure_height((100, 400), (102, 500), (101, 200))

    def test_hip_outside_segment_is_rejected(self):
        with self.assertRaises(ValueError):
            measure_height((100, 400), (800, 400), (900, 160))

    def test_invalid_scales_are_rejected(self):
        for scale in (0, -1, float('nan'), float('inf')):
            with self.subTest(scale=scale):
                with self.assertRaises(ValueError):
                    measure_height((100, 400), (800, 400), (450, 160), scale)

    def test_nonfinite_point_is_rejected(self):
        with self.assertRaises(ValueError):
            measure_height((100, 400), (800, 400), (float('nan'), 160))


if __name__ == '__main__':
    unittest.main()
