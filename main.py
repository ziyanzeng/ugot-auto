import time
import cv2
import queue
from threading import Thread, Condition
from camera import UGOTCamera
from model import YOLOModel
from threads.camera_thread import camera_thread
from threads.control_thread import control_thread
import config
from ugot import ugot
from logger import logger  # Import the global logger

def main():
    # Log the start of the main function
    logger.info('Main function started')

    # Robot connection configuration
    got = ugot.UGOT()
    got.initialize(config.UGOT_IP)
    cam = UGOTCamera(got)
    cam.open_camera()

    model = YOLOModel(config.MODEL_PATH)

    # Render queue configuration
    render_frame_queue = queue.Queue(maxsize=1)  # Only allow one frame in the queue

    # Initialize condition variable
    condition = Condition()

    # Invoke camera thread
    camera_thread_instance = Thread(target=camera_thread, args=(got, cam, model, render_frame_queue, condition))
    camera_thread_instance.start()
    
    # # Invoke control thread
    # control_thread_instance = Thread(target=control_thread, args=(got,))
    # control_thread_instance.start()

    # Show rendered frames in main thread
    while True:
        with condition:
            start_time = time.time()
            condition.wait()  # Wait for notification from the camera thread
            if render_frame_queue.empty():
                continue
            frame = render_frame_queue.get()
            if frame is None:
                break
            # Frame is not None
            cv2.namedWindow('YOLOv8 Ball Detection', cv2.WINDOW_NORMAL)
            cv2.imshow('YOLOv8 Ball Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                with config.shared_data["lock"]:
                    config.shared_data["exit"] = True
                break
            end_time = time.time()
            logger.info(f'Frame displayed. FPS: {1 / (end_time - start_time)}')

    cv2.destroyAllWindows()
    logger.info('Main thread exited')

    # End thread
    camera_thread_instance.join()
    # control_thread_instance.join()

if __name__ == "__main__":
    main()
