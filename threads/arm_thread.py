import time

def arm_thread(got, control_signal):
    while True:
        with control_signal:
            control_signal.wait()
            
        # 关节角度控制
        got.mechanical_joint_control(0, 0, -90, 500)
        time.sleep(0.5)

        got.mechanical_joint_control(0, -40, -90, 500)
        time.sleep(0.5)

        got.mechanical_joint_control(0, 0, 0, 20)
        time.sleep(0.02)

        # 移动位置
        got.mechanical_move_axis(10.0, 9.0, 0.0, 1000)
        time.sleep(1)

        # 机械臂复位
        got.mechanical_arms_restory()
        time.sleep(1)