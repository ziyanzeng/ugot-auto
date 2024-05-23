import time
import cv2
import numpy as np
from threading import Thread, Lock
from camera import UGOTCamera
from model import YOLOModel
from utils import calculate_relative_position_params, draw_max_score_detection, get_single_relative_pos
import config
from ugot import ugot

# 全局变量，用于共享数据
shared_data = {
    "frame": None,
    "detections": None,
    "frame_width": 0,
    "frame_height": 0,
    "exit": False,
}
data_lock = Lock()

class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def update(self, error):
        self.integral += error
        derivative = error - self.prev_error
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative

    def set_pid(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

def camera_loop(got, cam, model):
    while True:
        with data_lock:
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

        with data_lock:
            shared_data["frame"] = graphic.copy()
            shared_data["detections"] = detections
            shared_data["frame_width"] = frame_width
            shared_data["frame_height"] = frame_height

        graphic = draw_max_score_detection(graphic, detections, frame_width, frame_height)

        try:
            cv2.imshow('YOLOv8 Ball Detection', graphic)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                with data_lock:
                    shared_data["exit"] = True
                break
        except cv2.error as e:
            print("OpenCV error:", e)
            break

    cam.close_camera()
    cv2.destroyAllWindows()

def control_loop(got, pid):
    while True:
        with data_lock:
            if shared_data["exit"]:
                break
            if shared_data["detections"] is not None:
                frame_width = shared_data["frame_width"]
                frame_height = shared_data["frame_height"]
                detections = shared_data["detections"]

                distance, angle = get_single_relative_pos(detections, frame_width, frame_height)

                # 将角度限制在[-180, 180]范围内
                angle = angle % 360
                if angle > 180:
                    angle -= 360

                if angle < -1 or angle > 1:
                    turn_speed = abs(pid.update(angle))
                    turn_speed = min(turn_speed, 280)  # 限制最大转速
                    if angle < -1:
                        got.mecanum_turn_speed(2, turn_speed)  # 左转
                    elif angle > 1:
                        got.mecanum_turn_speed(3, turn_speed)  # 右转
                else:
                    got.mecanum_stop()  # 停止转动

        time.sleep(0.1)  # 控制循环间隔

def display_loop():
    cv2.namedWindow('YOLOv8 Ball Detection', cv2.WINDOW_NORMAL)
    
    while True:
        with data_lock:
            if shared_data["exit"]:
                break
            frame = shared_data["frame"]

        if frame is not None:
            cv2.imshow('YOLOv8 Ball Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                with data_lock:
                    shared_data["exit"] = True
                break

    cv2.destroyAllWindows()

def main():
    got = ugot.UGOT()
    got.initialize(config.UGOT_IP)
    cam = UGOTCamera(got)
    cam.open_camera()

    model = YOLOModel(config.MODEL_PATH)

    # 创建PID控制器
    pid = PID(kp=0.1, ki=0.01, kd=0.05)

    # 启动摄像头读取和检测线程
    camera_thread = Thread(target=camera_loop, args=(got, cam, model))
    camera_thread.start()

    # 启动控制线程
    control_thread = Thread(target=control_loop, args=(got, pid))
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
