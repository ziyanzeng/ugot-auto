import math
from utils import parse_detection_results
from utils import calculate_relative_position_params
import config
import numpy as np

def get_single_relative_pos(detections, frame_width, frame_height):
    boxes, scores, classes = parse_detection_results(detections)
    max_index = np.argmax(scores)
    box = boxes[max_index]
    x1, y1, x2, y2 = map(int, box)
    distance, angle = calculate_relative_position_params(config.BALL_DIAMETER, config.CAM_FOCAL, config.SENSOR_WIDTH, config.SENSOR_HEIGHT, frame_width / 2, frame_height / 2, x1, y1, x2, y2)
    return distance, angle