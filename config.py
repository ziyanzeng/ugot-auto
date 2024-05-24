# system params
UGOT_IP = "10.10.67.69"
MODEL_PATH = './model/ball.pt'
CLASS_LABELS = {0: 'pingpong', 1: 'tennis'}

# detection constants
BALL_DIAMETER = 40 #pingpong ball diameter, change if model switched to tennis
CAM_FOCAL = 20
SENSOR_WIDTH = 5.7
SENSOR_HEIGHT = 7.6

# PID Constants
angle_kp = 0.1
angle_ki = 0.01
angle_kd = 0.05
translation_kp = 0.1
translation_ki = 0.01
translation_kd = 0.05