import time
import cv2
import numpy as np
from camera import UGOTCamera
from model import YOLOModel
from utils import calculate_relative_position_params, draw_detections, draw_max_score_detection
import config
from ugot import ugot

def main():
    got = ugot.UGOT()
    got.initialize(config.UGOT_IP)
    cam = UGOTCamera(got)
    cam.open_camera()

    model = YOLOModel(config.MODEL_PATH)
    
    # got.mecanum_turn_speed_times(2, 30, 1, 2)

    while True:
        frame = cam.read_camera_data()
        if frame is None:
            break

        nparr = np.frombuffer(frame, np.uint8)
        data = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if data is None:
            print("Failed to decode image")
            continue

        frame_height, frame_width = data.shape[:2]

        results = model.predict(data)
        detections = results[0]

        data = draw_max_score_detection(data, detections, frame_width, frame_height)

        cv2.imshow('YOLOv8 Ball Detection', data)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
