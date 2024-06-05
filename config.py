# system params
UGOT_IP = "10.10.64.179"
MODEL_PATH = './model/best3.pt'
CLASS_LABELS = {0: 'goal', 1: 'ping-pong', 2: 'ping-pong-partial'}

# detection constants
BALL_DIAMETER = 40  # pingpong ball diameter, change if model switched to tennis
GOAL_WIDTH = 235
CAM_FOCAL = 20
SENSOR_WIDTH = 5.7
SENSOR_HEIGHT = 7.6

PANEL_ENABLE = True

LINEAR_KP = 1.25
LINEAR_KI = 0.005
LINEAR_KD = 0.05
ANGLE_KP = 1.0
ANGLE_KI = 0.035
ANGLE_KD = 0.1
PIVOT_KP = 1.0
PIVOT_KI = 10
PIVOT_KD = 0.1