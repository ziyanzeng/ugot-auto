import cv2
import numpy as np
import utils
from config import shared_data
from logger import logger  # Import the global logger
import threading
import time
import base64

def camera_thread(got, cam, model, render_frame_queue, condition, ws_server):
    prev_time = time.time()
    
    while True:
        with shared_data["lock"]:
            if shared_data["exit"]:
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

        with shared_data["lock"]:
            shared_data["frame"] = graphic.copy()
            shared_data["detections"] = detections
            shared_data["frame_width"] = frame_width
            shared_data["frame_height"] = frame_height

        graphic = utils.draw_max_score_detection(graphic, detections)

        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time)
        prev_time = curr_time
        
        # Check queue size, remove old elements if it exceeds the maximum size
        while render_frame_queue.qsize() >= 1:  # Ensure only one frame in the queue
            render_frame_queue.get()
            
        # Display FPS on the frame
        cv2.putText(graphic, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Encode the frame to JPEG
        _, jpeg = cv2.imencode('.jpg', graphic)
        jpeg_bytes = jpeg.tobytes()
        jpeg_base64 = base64.b64encode(jpeg_bytes).decode('utf-8')

        # Put the processed frame into the render queue
        render_frame_queue.put(graphic)

        # Send the frame to the WebSocket server
        ws_server.send_video_frame(jpeg_base64)

        # Notify the main thread
        with condition:
            condition.notify_all()

    cam.close_camera()
    logger.info('Camera thread exited')
