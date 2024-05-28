from threading import Lock
from utils import PID

shared_data = {
    "frame": None,
    "detections": None,
    "distance": 0,
    "angle": 0,
    "distance_history": [],
    "angle_history": [],
    "lock": Lock(),
    "exit": False,
    "linear_pid": PID(1.0, 0.01, 0.05),
    "angle_pid": PID(1.0, 0.01, 0.05)
}

# system params
UGOT_IP = "10.10.67.69"
MODEL_PATH = './model/ball.pt'
CLASS_LABELS = {0: 'pingpong', 1: 'tennis'}

# detection constants
BALL_DIAMETER = 40 #pingpong ball diameter, change if model switched to tennis
CAM_FOCAL = 20
SENSOR_WIDTH = 5.7
SENSOR_HEIGHT = 7.6
