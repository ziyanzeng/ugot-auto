import cv2
import numpy as np
import utils
from config import shared_data, logger

MAX_QUEUE_SIZE = 10  # 设置一个合适的最大队列大小

def camera_thread(got, cam, model, render_frame_queue):
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

        graphic = utils.draw_max_score_detection(graphic, detections, frame_width, frame_height)

        # 检查队列大小，如果超过最大值则移除旧元素
        while render_frame_queue.qsize() >= MAX_QUEUE_SIZE:
            render_frame_queue.get()

        # 将处理完的画面存入缓存队列
        render_frame_queue.put(graphic)

        logger.info('Frame processed and added to queue')

    cam.close_camera()
    logger.info('Camera thread exited')
