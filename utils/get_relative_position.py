import math
from utils.parse_results import parse_detection_results
import config
import numpy as np
from shared_data import SharedData
from logger import logger

def get_single_relative_pos(detections, class_name):
    boxes, scores, classes = parse_detection_results(detections)
    if len(scores) == 0:
        return 0, 0, None, 0, 0
    class_indices = [i for i, c in enumerate(classes) if config.CLASS_LABELS[int(c)] == class_name]
    if not class_indices:
        return 0, 0, None, 0, 0
    max_index = max(class_indices, key=lambda i: scores[i])
    box = boxes[max_index]
    x1, y1, x2, y2 = map(int, box)
    # logger.info(f"class indices: {class_indices}, box data: {x1}, {x2}, {y1}, {y2}")
    distance, angle = calculate_relative_position_params(config.BALL_DIAMETER if class_name == "ping-pong" or class_name == "ping-pong-partial" else config.GOAL_WIDTH, config.CAM_FOCAL, config.SENSOR_WIDTH, config.SENSOR_HEIGHT, SharedData.shared_data["frame_width"] / 2, SharedData.shared_data["frame_height"] / 2, x1, y1, x2, y2)
    return distance, angle, box, scores[max_index], classes[max_index]

def calculate_relative_position_params(actual_width, focal_length, sensor_width, sensor_height, image_center_x, image_center_y, x1, y1, x2, y2):
    pixel_width = abs(x1 - x2)
    pixel_height = abs(y1 - y2)
    pixel_x = abs(x1 + x2) / 2
    pixel_y = abs(y1 + y2) / 2
    
    if abs(pixel_width - pixel_height) / max(pixel_width, pixel_height) < 0.2:
        pixel_width = (pixel_width + pixel_height) / 2
    else:
        pixel_width = max(pixel_width, pixel_height)
        pixel_x = x2 - pixel_width / 2 if x1 == 0 else x1 + pixel_width / 2
    
    sensor_x = (pixel_x - image_center_x) * sensor_width / (2 * image_center_x)
    theta_x = math.atan(sensor_x / focal_length)
    horizontal_distance = (actual_width * focal_length) / ((pixel_width * sensor_width / (image_center_x * 2)) * math.cos(theta_x))
    
    if (x1 < 5 or x2 > image_center_x * 2 - 5) and (y1 > image_center_y * 2 - 5 or y2 > image_center_y * 2 - 5):
        #logger.info("Object in the corner, returning (0, angle)")
        return 0, math.degrees(theta_x * 4.56)
    
    return abs((horizontal_distance / 1000 - 0.09) / 0.033), math.degrees(theta_x * 4.56)