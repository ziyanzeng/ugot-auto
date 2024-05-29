from .Command import Command
from .actuators.chassis import Chassis
from shared_data import shared_data
from logger import logger

class LocateBallCommand(Command):
    def __init__(self, got, pid_controllers=None):
        super().__init__(got, pid_controllers)
        self.chassis = Chassis(got)
        self.angle_pid = self.pid_controllers.get('angle', None)
        self.cummulate = 0

    def initialize(self):
        self.finished = False

    def execute(self):
        self.cummulate += 1
        # end only when target is found
        if shared_data["detections"] is not None and (shared_data["angle"] != 0 or shared_data["distance"] != 0) or self.cummulate > 1000:
            self.end()
        else:
            turn_speed = 75
            self.chassis.spin_on_location(turn_speed)

    def end(self):
        self.finished = True
        self.chassis.stop()

    def isFinished(self):
        return self.finished
