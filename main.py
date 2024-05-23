import time
import cv2
import numpy as np
from camera.camera import UGOTCamera
from model.model import YOLOModel
from utils.calculations import calculate_relative_position_params
from utils.drawing import draw_detections
import config

def main():
    got = UGOTCamera(config.CAMERA_IP)
    got.open_camera()

    model = YOLOModel(config.MODEL_PATH)

    while True:
        frame = got.read_camera_data()
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

        data = draw_detections(data, detections, frame_width, frame_height)

        cv2.imshow('YOLOv8 Ball Detection', data)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
