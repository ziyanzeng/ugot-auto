import time
from logger import logger

def arm_thread(got, control_signal):
    while True:
        with control_signal:
            control_signal.wait()
            
        logger.info("kick signal received. Starting routine...")
            
        # 关节角度控制
        got.mechanical_joint_control(-35, 0, -90, 500)
        time.sleep(0.5)
        
        got.mechanical_joint_control(0, -40, -90, 500)
        time.sleep(0.5)

        got.mechanical_joint_control(0, 0, 0, 200)
        time.sleep(0.2)

        # 机械臂复位
        got.mechanical_arms_restory()
        time.sleep(1)
        
        logger.info("kick routine ended, waiting for next signal...")