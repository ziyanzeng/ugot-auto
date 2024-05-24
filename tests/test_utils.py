import unittest
import utils
import cv2
import numpy as np

class TestUtils(unittest.TestCase):
    def test_calculate_relative_position_params(self):
        actual_width = 40
        focal_length = 20
        sensor_width = 5.7
        sensor_height = 7.6
        image_center_x = 320
        image_center_y = 240
        x1, y1, x2, y2 = 100, 100, 200, 200

        distance, angle = utils.calculate_relative_position_params(
            actual_width, focal_length, sensor_width, sensor_height,
            image_center_x, image_center_y, x1, y1, x2, y2
        )
        self.assertGreater(distance, 0)
        self.assertIsNotNone(angle)

    def test_draw_max_score_detection(self):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        detections = {'boxes': [{'xyxy': [100, 100, 200, 200], 'score': 0.9, 'cls': 0}]}
        frame_width = 640
        frame_height = 480

        result_frame = utils.draw_max_score_detection(frame, detections, frame_width, frame_height)
        self.assertEqual(result_frame.shape, frame.shape)

if __name__ == '__main__':
    unittest.main()
