from .Command import Command
from .actuators.chassis import Chassis

class TranslateToBallCommand(Command):
    def __init__(self, got, shared_data, distance, angle, pid_controllers=None):
        super().__init__(got, shared_data, pid_controllers)
        self.chassis = Chassis(got)
        self.distance = distance
        self.angle = angle
        self.linear_pid = self.pid_controllers.get('linear', None)

    def initialize(self):
        self.finished = False

    def execute(self):
        with self.shared_data["lock"]:
            if self.distance < 10:
                self.finished = True
                self.chassis.stop()
            else:
                speed = self.linear_pid.update(self.distance) if self.linear_pid else 20
                self.chassis.translate(self.angle, speed)

    def end(self):
        self.chassis.stop()

    def isFinished(self):
        return self.finished
