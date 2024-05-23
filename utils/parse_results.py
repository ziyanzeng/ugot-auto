import numpy as np

def parse_detection_results(detections):
    boxes = detections.boxes.xyxy.cpu().numpy()
    scores = detections.boxes.conf.cpu().numpy()
    classes = detections.boxes.cls.cpu().numpy()
    return boxes, scores, classes