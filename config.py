# system params
UGOT_IP = "10.10.64.132"
MODEL_PATH = './model/best.pt'
CLASS_LABELS = {0: 'goal', 1: 'ping-pong'}

# detection constants
BALL_DIAMETER = 40  # pingpong ball diameter, change if model switched to tennis
GOAL_WIDTH = 235
CAM_FOCAL = 20
SENSOR_WIDTH = 5.7
SENSOR_HEIGHT = 7.6

PANEL_ENABLE = True