import cv2
import math
from utils import parse_detection_results
from utils import get_single_relative_pos
import numpy as np
import config

# draw only the box with the highest confidence
def draw_max_score_detection(data, detections):
    boxes, scores, classes = parse_detection_results(detections)

    if len(scores) == 0:
        return data

    max_index = np.argmax(scores)
    box = boxes[max_index]
    score = scores[max_index]
    cls = classes[max_index]

    x1, y1, x2, y2 = map(int, box)
    label = f'{config.CLASS_LABELS[int(cls)]}: {score:.2f}'
    color = (0, 255, 0) if cls == 0 else (255, 0, 0)
    
    distance, angle = get_single_relative_pos(detections)
    distance_label = f'distance: {distance:.2f}'
    angle_label = f'angle: {angle:.2f}'
    
    cv2.rectangle(data, (x1, y1), (x2, y2), color, 2)
    cv2.putText(data, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    cv2.putText(data, distance_label, (x1, y1 - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    cv2.putText(data, angle_label, (x1, y1 - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    
    return data