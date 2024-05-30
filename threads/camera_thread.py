import cv2
import numpy as np
import utils
from shared_data import SharedData
from logger import logger  # Import the global logger
import time

import utils.drawing

def camera_thread(got, cam, model, render_frame_queue, condition):
    prev_time = time.time()
    
    while True:
        with SharedData.shared_data["lock"]:
            if SharedData.shared_data["exit"]:
                break

        frame = cam.read_camera_data()
        if frame is None:
            logger.error('No camera data received')
            break

        nparr = np.frombuffer(frame, np.uint8)
        graphic = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if graphic is None:
            logger.error('Failed to decode image')
            continue

        frame_height, frame_width = graphic.shape[:2]

        results = model.predict(graphic)
        detections = results[0]

        with SharedData.shared_data["lock"]:
            SharedData.shared_data["frame"] = graphic.copy()
            SharedData.shared_data["detections"] = detections
            SharedData.shared_data["frame_width"] = frame_width
            SharedData.shared_data["frame_height"] = frame_height

        graphic = utils.drawing.draw_max_score_detection(graphic, detections)

        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time)
        prev_time = curr_time
        
        # Check queue size, remove old elements if it exceeds the maximum size
        while render_frame_queue.qsize() >= 1:  # Ensure only one frame in the queue
            render_frame_queue.get()
            
        # Display FPS on the frame
        cv2.putText(graphic, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Put the processed frame into the render queue
        render_frame_queue.put(graphic)

        # Notify the main thread
        with condition:
            condition.notify_all()

        # logger.info('Frame processed and added to queue')
        with SharedData.shared_data["lock"]:
            SharedData.shared_data["latest_frame"] = graphic

    cam.close_camera()
    logger.info('Camera thread exited')
