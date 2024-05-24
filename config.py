from threading import Lock

shared_data = {
    "frame": None,
    "detections": None,
    "frame_width": 0,
    "frame_height": 0,
    "lock": Lock(),
    "exit": False,
}

# system params
UGOT_IP = "10.10.67.69"
MODEL_PATH = './model/ball.pt'
CLASS_LABELS = {0: 'pingpong', 1: 'tennis'}

# detection constants
BALL_DIAMETER = 40 # pingpong ball diameter, change if model switched to tennis
CAM_FOCAL = 20
SENSOR_WIDTH = 5.7
SENSOR_HEIGHT = 7.6
