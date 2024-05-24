import unittest
from camera import UGOTCamera
from ugot import ugot
import config

class TestUGOTCamera(unittest.TestCase):
    def setUp(self):
        self.got = ugot.UGOT()
        self.got.initialize(config.UGOT_IP)
        self.cam = UGOTCamera(self.got)

    def test_open_camera(self):
        self.assertTrue(self.cam.open_camera())

    def test_read_camera_data(self):
        self.cam.open_camera()
        data = self.cam.read_camera_data()
        self.assertIsNotNone(data)

    def test_close_camera(self):
        self.cam.open_camera()
        self.cam.close_camera()
        self.assertFalse(self.cam.read_camera_data())

if __name__ == '__main__':
    unittest.main()
