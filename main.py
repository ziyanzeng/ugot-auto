import time
import cv2
import queue
from threading import Thread, Condition, Event
import signal
from camera import UGOTCamera
from model import YOLOModel
from threads.camera_thread import camera_thread
from threads.control_thread import control_thread
from threads.arm_thread import arm_thread
from shared_data import SharedData
import config
from ugot import ugot
from logger import logger  # Import the global logger
from ws_server import start_server

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

    # Initialize condition variables
    condition = Condition()

    # Create shutdown event
    shutdown_event = Event()

    # Signal handler to set shutdown event
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, initiating shutdown...")
        shutdown_event.set()

    # Set up signal handling in the main thread
    for signame in ('SIGINT', 'SIGTERM'):
        signal.signal(getattr(signal, signame), signal_handler)

    # Start WebSocket server
    ws_thread = Thread(target=start_server, args=(shutdown_event,))
    ws_thread.start()

    # Invoke camera thread
    camera_thread_instance = Thread(target=camera_thread, args=(got, cam, model, render_frame_queue, condition))
    camera_thread_instance.start()

    # Invoke control thread
    control_thread_instance = Thread(target=control_thread, args=(got, condition))
    control_thread_instance.start()
    
    # Invoke arm thread
    arm_thread_instance = Thread(target=arm_thread, args=(got))
    arm_thread_instance.start()

    # Show rendered frames in main thread
    while not shutdown_event.is_set():
        with condition:
            condition.wait(1)  # Wait for notification from the camera thread with a timeout
            if render_frame_queue.empty():
                continue
            frame = render_frame_queue.get()
            if frame is None:
                break
            # Frame is not None
            cv2.namedWindow('YOLOv8 Ball Detection', cv2.WINDOW_NORMAL)
            cv2.imshow('YOLOv8 Ball Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                with SharedData.shared_data["lock"]:
                    SharedData.shared_data["exit"] = True
                shutdown_event.set()
                break
            # logger.info('Frame displayed.')

    cv2.destroyAllWindows()
    logger.info('Main thread exited')

    # Signal other threads to shutdown
    shutdown_event.set()

    # End threads
    camera_thread_instance.join()
    control_thread_instance.join()
    arm_thread_instance.join()
    ws_thread.join()
    
    got.stop_chassis()

if __name__ == "__main__":
    main()
