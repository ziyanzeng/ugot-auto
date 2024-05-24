from .Command import Command
from .actuators.chassis import Chassis

class LocateBallCommand(Command):
    def __init__(self, got, shared_data, pid_controllers=None):
        super().__init__(got, shared_data, pid_controllers)
        self.chassis = Chassis(got)
        self.angle_pid = self.pid_controllers.get('angle', None)

    def initialize(self):
        self.finished = False

    def execute(self):
        with self.shared_data["lock"]:
            if self.shared_data["detections"] is not None:
                self.finished = True
                self.chassis.stop()
            else:
                turn_speed = self.angle_pid.update(30) if self.angle_pid else 30
                self.chassis.spin_on_location(turn_speed)

    def end(self):
        self.chassis.stop()

    def isFinished(self):
        return self.finished
