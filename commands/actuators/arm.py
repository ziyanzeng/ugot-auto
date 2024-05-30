from ugot import ugot

class Arm:
    def __init__(self, got):
        self.got = got
        
    def clamp_close(self):
        self.got.mechanical_clamp_release()
    
    def clamp_release(self):
        self.got.mechanical_clamp_close()
        
    def restore(self):
        self.got.mechanical_arms_restory()
        
    def joint_angle(self, shoulder, elbow, wrist, motion_duration):
        self.got.mechanical_joint_control(shoulder, elbow, wrist, motion_duration)
    