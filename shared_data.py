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
        "linear_pid": PID(1.0, 0.01, 0.05),
        "angle_pid": PID(1.0, 0.01, 0.05),
        "command": None,
        "distance": 0,
        "angle": 0,
        "distance_history": [0] * 50,
        "angle_history": [0] * 50
    }
