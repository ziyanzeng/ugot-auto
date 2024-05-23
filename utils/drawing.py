import cv2
import math
from utils.calculations import calculate_relative_position_params
import config

def draw_detections(data, detections, frame_width, frame_height):
    boxes = detections.boxes.xyxy.cpu().numpy()
    scores = detections.boxes.conf.cpu().numpy()
    classes = detections.boxes.cls.cpu().numpy()

    for (box, score, cls) in zip(boxes, scores, classes):
        if score > 0.5:
            x1, y1, x2, y2 = map(int, box)
            label = f'{config.CLASS_LABELS[int(cls)]}: {score:.2f}'
            color = (0, 200, 0) if cls == 0 else (200, 0, 0)
            
            distance, angle = calculate_relative_position_params(config.BALL_DIAMETER, config.CAM_FOCAL, config.SENSOR_WIDTH, config.SENSOR_HEIGHT, frame_width / 2, frame_height / 2, x1, y1, x2, y2)
            distance = (distance / 1000 - 0.09) / 0.033
            distance_label = f'distance: {distance:.2f}'
            angle = math.degrees(angle)
            angle_label = f'angle: {angle:.2f}'
            
            cv2.rectangle(data, (x1, y1), (x2, y2), color, 2)
            cv2.putText(data, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            cv2.putText(data, distance_label, (x1, y1 - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            cv2.putText(data, angle_label, (x1, y1 - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    
    return data

# draw only the box with the highest confidence
def draw_max_score_detection(data, detections, frame_width, frame_height):
    boxes = detections.boxes.xyxy.cpu().numpy()
    scores = detections.boxes.conf.cpu().numpy()
    classes = detections.boxes.cls.cpu().numpy()

    if len(scores) == 0:
        return data

    max_index = np.argmax(scores)
    box = boxes[max_index]
    score = scores[max_index]
    cls = classes[max_index]

    x1, y1, x2, y2 = map(int, box)
    label = f'{config.CLASS_LABELS[int(cls)]}: {score:.2f}'
    color = (0, 255, 0) if cls == 0 else (255, 0, 0)
    
    distance, angle = calculate_relative_position_params(config.BALL_DIAMETER, config.CAM_FOCAL, config.SENSOR_WIDTH, config.SENSOR_HEIGHT, frame_width / 2, frame_height / 2, x1, y1, x2, y2)
    distance = (distance / 1000 - 0.09) / 0.033
    distance_label = f'distance: {distance:.2f}'
    angle = math.degrees(angle)
    angle_label = f'angle: {angle:.2f}'
    
    cv2.rectangle(data, (x1, y1), (x2, y2), color, 2)
    cv2.putText(data, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    cv2.putText(data, distance_label, (x1, y1 - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    cv2.putText(data, angle_label, (x1, y1 - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    
    return data