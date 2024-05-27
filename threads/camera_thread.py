import cv2
import numpy as np
import utils
from config import shared_data
from logger import logger  # Import the global logger
import threading

def camera_thread(got, cam, model, render_frame_queue, condition):
    while True:
        with shared_data["lock"]:
            if shared_data["exit"]:
                break

        frame = cam.read_camera_data()
        logger.info('frame read from camera')
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
        logger.info('detections processed from camera frame')

        with shared_data["lock"]:
            shared_data["frame"] = graphic.copy()
            shared_data["detections"] = detections
            shared_data["frame_width"] = frame_width
            shared_data["frame_height"] = frame_height

        graphic = utils.draw_max_score_detection(graphic, detections, frame_width, frame_height)

        # Check queue size, remove old elements if it exceeds the maximum size
        while render_frame_queue.qsize() >= 1:  # Ensure only one frame in the queue
            render_frame_queue.get()

        # Put the processed frame into the render queue
        render_frame_queue.put(graphic)

        # Notify the main thread
        with condition:
            condition.notify_all()

        logger.info('Frame processed and added to queue')

    cam.close_camera()
    logger.info('Camera thread exited')
