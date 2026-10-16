import unittest
from measurement import metres_from_pixels, lip_y_at_x, pixel_height_above_lip


class MeasurementTest(unittest.TestCase):
    def test_no_calibration(self):
        self.assertIsNone(metres_from_pixels(150, 0))
        self.assertIsNone(metres_from_pixels(150, None))

    def test_calibration(self):
        self.assertEqual(metres_from_pixels(150, 50), 3)
        self.assertEqual(metres_from_pixels(-50, 50), 0)

    def test_lip_interpolation(self):
        self.assertAlmostEqual(lip_y_at_x((0, 100), (100, 200), 50), 150)

    def test_hip_above_lip(self):
        self.assertEqual(pixel_height_above_lip((50, 100), (0, 150), (100, 150)), 50)
        self.assertEqual(pixel_height_above_lip((50, 180), (0, 150), (100, 150)), 0)


if __name__ == "__main__":
    unittest.main()
