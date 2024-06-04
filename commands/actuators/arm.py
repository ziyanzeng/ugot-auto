from ugot import ugot
import time

class Arm:
    def __init__(self, got):
        self.got = got
        
    def clamp_close(self):
        self.got.mechanical_clamp_release()
    
    def clamp_release(self):
        self.got.mechanical_clamp_close()
        
    def restore(self):
        self.got.mechanical_arms_restory()
    
    def kick_motion(self):
        # 机械臂复位
        self.got.mechanical_arms_restory()
        self.got.mecanum_translate_speed(-180, 20)
        time.sleep(0.5)
        
        # 关节角度控制
        self.got.mechanical_joint_control(-15, 0, -90, 500)
        self.got.mecanum_translate_speed(0, 40)
        time.sleep(0.5)
        
        self.got.mechanical_joint_control(0, -30, -90, 200)
        time.sleep(0.2)

        self.got.mechanical_joint_control(0, 0, 20, 200)
        time.sleep(0.2)

        # 机械臂复位
        self.got.mechanical_arms_restory()
        time.sleep(1)
        
        return True
    