import cv2
import numpy as np
import utils
from config import shared_data

def camera_thread(got, cam, model, render_frame_queue):
    while True:
        with shared_data["lock"]:
            if shared_data["exit"]:
                break

        frame = cam.read_camera_data()
        if frame is None:
            break

        nparr = np.frombuffer(frame, np.uint8)
        graphic = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if graphic is None:
            print("Failed to decode image")
            continue

        frame_height, frame_width = graphic.shape[:2]

        results = model.predict(graphic)
        detections = results[0]

        with shared_data["lock"]:
            shared_data["frame"] = graphic.copy()
            shared_data["detections"] = detections
            shared_data["frame_width"] = frame_width
            shared_data["frame_height"] = frame_height

        graphic = utils.draw_max_score_detection(graphic, detections, frame_width, frame_height)

        # 将处理完的画面存入缓存队列
        render_frame_queue.put(graphic)

    cam.close_camera()
