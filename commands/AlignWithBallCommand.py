from .Command import Command
from .actuators.chassis import Chassis
from config import shared_data

class AlignWithBallCommand(Command):
    def __init__(self, got, pid_controllers=None):
        super().__init__(got, pid_controllers)
        self.chassis = Chassis(got)
        self.angle_pid = self.pid_controllers.get('angle', None)

    def initialize(self):
        self.finished = False

    def execute(self):
        if abs(shared_data["angle"]) < 1:
            self.end()
        else:
            turn_speed = self.angle_pid.update(shared_data["angle"])
            self.chassis.spin_on_location(turn_speed)

    def end(self):
        self.finished = True
        self.chassis.stop()

    def isFinished(self):
        return self.finished
