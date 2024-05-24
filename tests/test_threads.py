import unittest
import queue
from threading import Thread
from ugot import ugot
from camera import UGOTCamera
from model import YOLOModel
from threads.camera_thread import camera_thread
from threads.control_thread import control_thread
from utils.render_frame import RenderFrame
import config

class TestThreads(unittest.TestCase):
    def setUp(self):
        self.got = ugot.UGOT()
        self.cam = UGOTCamera(self.got)
        self.model = YOLOModel(config.MODEL_PATH)
        self.render_frame_queue = queue.Queue()

    def test_camera_thread(self):
        camera_thread_instance = Thread(target=camera_thread, args=(self.got, self.cam, self.model, self.render_frame_queue))
        camera_thread_instance.start()
        camera_thread_instance.join()
        self.assertTrue(camera_thread_instance.is_alive())

    def test_control_thread(self):
        control_thread_instance = Thread(target=control_thread, args=(self.got,))
        control_thread_instance.start()
        control_thread_instance.join()
        self.assertTrue(control_thread_instance.is_alive())

    def test_render_frame(self):
        render_thread_instance = RenderFrame("RenderFrame", self.render_frame_queue)
        render_thread_instance.start()
        render_thread_instance.join()
        self.assertTrue(render_thread_instance.is_alive())

if __name__ == '__main__':
    unittest.main()
