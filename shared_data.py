import threading
from utils.pid_controller import PID

class SharedData:
    shared_data = {
        "frame": None,
        "detections": None,
        "frame_width": 0,
        "frame_height": 0,
        "lock": threading.Lock(),
        "exit": False,
        "linear_pid": PID(1.25, 0.005, 0.05),
        "angle_pid": PID(1.0, 0.035, 0.1),
        "command": None,
        "distance": 0,
        "angle": 0,
        "distance_history": [0] * 50,
        "angle_history": [0] * 50,
        "latest_frame": None,
        "distance_goal": 0,
        "angle_goal": 0,
        "restart_trial": False
    }
