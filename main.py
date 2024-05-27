import time
import cv2
import queue
from threading import Thread
from camera import UGOTCamera
from model import YOLOModel
from threads.render_thread import RenderFrame
from threads.camera_thread import camera_thread
from threads.control_thread import control_thread
import config
from ugot import ugot

def main():
    got = ugot.UGOT()
    got.initialize(config.UGOT_IP)
    cam = UGOTCamera(got)
    cam.open_camera()

    model = YOLOModel(config.MODEL_PATH)

    # 创建一个渲染完成的缓冲队列
    render_frame_queue = queue.Queue()

    # 启动摄像头读取和检测线程
    camera_thread_instance = Thread(target=camera_thread, args=(got, cam, model, render_frame_queue))
    camera_thread_instance.start()

    # 启动控制线程
    control_thread_instance = Thread(target=control_thread, args=(got,))
    control_thread_instance.start()

    # 启动渲染线程
    render_thread_instance = RenderFrame("RenderFrame", render_frame_queue)
    render_thread_instance.start()

    # 在主线程处理渲染完成的画面
    while True:
        frame = render_frame_queue.get()
        if frame is None:
            break
        start_time = time.time()
        # 如果获取的帧不为空
        cv2.namedWindow('YOLOv8 Ball Detection', cv2.WINDOW_NORMAL)
        cv2.imshow('YOLOv8 Ball Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            with config.shared_data["lock"]:
                config.shared_data["exit"] = True
            break
        end_time = time.time()
        print("FPS: ", 1 / (end_time - start_time))

    cv2.destroyAllWindows()

    # 等待线程结束
    camera_thread_instance.join()
    control_thread_instance.join()
    render_thread_instance.join()

if __name__ == "__main__":
    main()
