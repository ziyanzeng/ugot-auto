import unittest
from unittest.mock import MagicMock, patch
import queue
from threading import Thread
import time
from ugot import ugot
from commands.CommandPlanner import CommandPlanner
from utils.pid_controller import PID
from threads.control_thread import control_thread
import config

class TestControlThread(unittest.TestCase):
    def setUp(self):
        self.got = MagicMock()
        self.shared_data = config.shared_data
        self.shared_data["detections"] = MagicMock()  # 使用 MagicMock 模拟 detections 对象
        self.shared_data["detections"].boxes.xyxy.cpu().numpy.return_value = [[100, 100, 200, 200]]
        self.shared_data["detections"].scores.cpu().numpy.return_value = [0.9]
        self.shared_data["detections"].cls.cpu().numpy.return_value = [0]
        self.shared_data["frame_width"] = 640
        self.shared_data["frame_height"] = 480

        # Create PID controllers
        self.pid_linear = PID(kp=0.1, ki=0.01, kd=0.05)
        self.pid_angle = PID(kp=0.1, ki=0.01, kd=0.05)
        self.pid_controllers = {
            "linear": self.pid_linear,
            "angle": self.pid_angle
        }

    @patch('commands.CommandPlanner.CommandPlanner.update')
    def test_control_thread(self, mock_update):
        # Mock the CommandPlanner
        command_planner = CommandPlanner(self.got, self.shared_data, self.pid_controllers)
        command_planner.update = mock_update

        # Run the control thread for a short period
        control_thread_instance = Thread(target=control_thread, args=(self.got,))
        control_thread_instance.start()
        
        time.sleep(0.5)  # Let the thread run for a short time
        
        with self.shared_data["lock"]:
            self.shared_data["exit"] = True

        control_thread_instance.join()

        # Verify that the update method was called
        self.assertTrue(mock_update.called)
        self.assertGreater(mock_update.call_count, 0)

if __name__ == '__main__':
    unittest.main()
