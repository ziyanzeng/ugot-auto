from .Command import Command
from .actuators.chassis import Chassis
from config import shared_data

class TranslateToBallCommand(Command):
    def __init__(self, got, distance, angle, pid_controllers=None):
        super().__init__(got, pid_controllers)
        self.chassis = Chassis(got)
        self.distance = distance
        self.angle = angle
        self.linear_pid = self.pid_controllers.get('linear', None)

    def initialize(self):
        self.finished = False

    def execute(self):
        with shared_data["lock"]:
            if self.distance < 10:
                self.end()
            else:
                speed = self.linear_pid.update(self.distance) if self.linear_pid else 20
                self.chassis.translate(self.angle, speed)

    def end(self):
        self.finished = True
        self.chassis.stop()

    def isFinished(self):
        return self.finished
