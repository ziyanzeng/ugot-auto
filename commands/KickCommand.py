from commands.Command import Command
from commands.actuators.arm import Arm

class KickCommand(Command):
    def __init__(self, got):
        self.got = got
        self.arm = Arm(self.got)
        
    def initialize(self):
        self.arm.kick_motion()
        
    def execute(self):
        self.isFinished = True
        
    def end(self):
        return
    
    def isFinished(self):
        return self.isFinished