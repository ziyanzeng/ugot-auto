from .Command import Command
from .actuators.chassis import Chassis

class AlignWithBallCommand(Command):
    def __init__(self, got, shared_data, angle, pid_controllers=None):
        super().__init__(got, shared_data, pid_controllers)
        self.chassis = Chassis(got)
        self.angle = angle
        self.angle_pid = self.pid_controllers.get('angle', None)

    def initialize(self):
        self.finished = False

    def execute(self):
        with self.shared_data["lock"]:
            if abs(self.angle) < 1:
                self.finished = True
                self.chassis.stop()
            else:
                turn_speed = self.angle_pid.update(self.angle) if self.angle_pid else 30
                self.chassis.spin_on_location(turn_speed)

    def end(self):
        self.chassis.stop()

    def isFinished(self):
        return self.finished
