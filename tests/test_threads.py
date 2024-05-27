import unittest
import queue
from threading import Thread
from ugot import ugot
from camera import UGOTCamera
from model.model import YOLOModel
from threads.camera_thread import camera_thread
from threads.control_thread import control_thread
from threads.render_thread import RenderFrame
import config
import time

class TestThreads(unittest.TestCase):
    def setUp(self):
        self.got = ugot.UGOT()
        self.got.initialize(config.UGOT_IP)
        self.cam = UGOTCamera(self.got)
        self.model = YOLOModel(config.MODEL_PATH)
        self.render_frame_queue = queue.Queue()
        self.shared_data = config.shared_data

    def test_camera_thread(self):
        camera_thread_instance = Thread(target=camera_thread, args=(self.got, self.cam, self.model, self.render_frame_queue))
        camera_thread_instance.start()
        
        # 等待一段时间以确保摄像头数据接收
        start_time = time.time()
        timeout = 5  # 设置超时时间为5秒
        while time.time() - start_time < timeout:
            if not self.render_frame_queue.empty():
                frame = self.render_frame_queue.get()
                self.assertIsNotNone(frame)
                break
            time.sleep(0.1)
        
        with self.shared_data["lock"]:
            self.shared_data["exit"] = True
        camera_thread_instance.join()

    def test_control_thread(self):
        control_thread_instance = Thread(target=control_thread, args=(self.got,))
        control_thread_instance.start()
        
        # 运行一段时间以检查控制线程
        time.sleep(2)
        
        with self.shared_data["lock"]:
            self.shared_data["exit"] = True
        control_thread_instance.join()

    def test_render_frame(self):
        render_thread_instance = RenderFrame("RenderFrame", self.render_frame_queue)
        render_thread_instance.start()
        
        # 运行一段时间以检查渲染线程
        time.sleep(2)
        
        with self.shared_data["lock"]:
            self.shared_data["exit"] = True
        render_thread_instance.join()

if __name__ == '__main__':
    unittest.main()
