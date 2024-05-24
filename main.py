import time
import cv2
import numpy as np
from threading import Thread, Lock
from camera import UGOTCamera
from model import YOLOModel
import utils
from commands.CommandPlanner import CommandPlanner
import config
from ugot import ugot

# 全局变量，用于共享数据
shared_data = {
    "frame": None,
    "detections": None,
    "frame_width": 0,
    "frame_height": 0,
    "lock": Lock(),
    "exit": False,
}

def camera_loop(got, cam, model):
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

        try:
            cv2.imshow('YOLOv8 Ball Detection', graphic)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                with shared_data["lock"]:
                    shared_data["exit"] = True
                break
        except cv2.error as e:
            print("OpenCV error:", e)
            break

    cam.close_camera()
    cv2.destroyAllWindows()

def control_loop(got):
    # 创建PID控制器
    pid_align = utils.PID(kp=0.1, ki=0.01, kd=0.05)
    pid_controllers = {"align": pid_align}

    command_planner = CommandPlanner(got, shared_data, pid_controllers)

    while True:
        with shared_data["lock"]:
            if shared_data["exit"]:
                break

            if shared_data["detections"] is not None:
                frame_width = shared_data["frame_width"]
                frame_height = shared_data["frame_height"]
                detections = shared_data["detections"]

                distance, angle = utils.get_single_relative_pos(detections, frame_width, frame_height)
                command_planner.update(distance, angle)

        time.sleep(0.1)  # 控制循环间隔

def display_loop():
    cv2.namedWindow('YOLOv8 Ball Detection', cv2.WINDOW_NORMAL)
    
    while True:
        with shared_data["lock"]:
            if shared_data["exit"]:
                break
            frame = shared_data["frame"]

        if frame is not None:
            cv2.imshow('YOLOv8 Ball Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                with shared_data["lock"]:
                    shared_data["exit"] = True
                break

    cv2.destroyAllWindows()

def main():
    got = ugot.UGOT()
    got.initialize(config.UGOT_IP)
    cam = UGOTCamera(got)
    cam.open_camera()

    model = YOLOModel(config.MODEL_PATH)

    # 启动摄像头读取和检测线程
    camera_thread = Thread(target=camera_loop, args=(got, cam, model))
    camera_thread.start()

    # 启动控制线程
    control_thread = Thread(target=control_loop, args=(got,))
    control_thread.start()

    # 启动显示线程
    display_thread = Thread(target=display_loop)
    display_thread.start()

    # 等待线程结束
    camera_thread.join()
    control_thread.join()
    display_thread.join()

if __name__ == "__main__":
    main()
