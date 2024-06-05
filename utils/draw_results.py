import cv2
import math
from utils.parse_results import parse_detection_results
from utils.get_relative_position import get_single_relative_pos
import numpy as np
import config
from shared_data import SharedData
from logger import logger

def draw_max_score_detection(data, detections):
    distance_ping_pong, angle_ping_pong, box_ping_pong, score_ping_pong, cls_ping_pong = get_single_relative_pos(detections, "ping-pong")
    distance_ping_pong_partial, angle_ping_pong_partial, box_ping_pong_partial, score_ping_pong_partial, cls_ping_pong_partial = get_single_relative_pos(detections, "ping-pong-partial")
    logger.info(f"full dist {distance_ping_pong}, full angle: {angle_ping_pong}")
    logger.info(f"part dist: {distance_ping_pong_partial}, part angle: {angle_ping_pong_partial}")
    # if confidence of partial ping pong is greater than confidence of entire ping pong, replace origianl data with partial detection data
    if score_ping_pong_partial > score_ping_pong:
        distance_ping_pong = distance_ping_pong_partial
        angle_ping_pong = angle_ping_pong_partial
        box_ping_pong = box_ping_pong_partial
        score_ping_pong = score_ping_pong_partial
    distance_goal, angle_goal, box_goal, score_goal, cls_goal = get_single_relative_pos(detections, "goal")
    SharedData.shared_data["distance"], SharedData.shared_data["angle"] = distance_ping_pong, angle_ping_pong
    SharedData.shared_data["distance_goal"], SharedData.shared_data["angle_goal"] = distance_goal, angle_goal
    data = draw_detection(data, distance_ping_pong, angle_ping_pong, box_ping_pong, score_ping_pong, 1)
    data = draw_detection(data, distance_goal, angle_goal, box_goal, score_goal, 0)
    
    return data

def draw_detection(data, distance, angle, box, score, cls):
        if box is None:
            return data
        x1, y1, x2, y2 = map(int, box)
        label = f'{config.CLASS_LABELS[int(cls)]}: {score:.2f}'
        color = (0, 255, 0) if config.CLASS_LABELS[int(cls)] == "ping-pong" else (255, 0, 0)
        
        distance_label = f'distance: {distance:.2f}'
        angle_label = f'angle: {angle:.2f}'
        
        cv2.rectangle(data, (x1, y1), (x2, y2), color, 2)
        cv2.putText(data, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        cv2.putText(data, distance_label, (x1, y1 - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        cv2.putText(data, angle_label, (x1, y1 - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        return data