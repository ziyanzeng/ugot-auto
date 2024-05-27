from .Command import Command
from .actuators.chassis import Chassis
from config import shared_data

class TranslateToBallCommand(Command):
    def __init__(self, got, pid_controllers=None):
        super().__init__(got, pid_controllers)
        self.chassis = Chassis(got)
        self.distance = shared_data["distance"]
        self.angle = shared_data["angle"]
        self.linear_pid = self.pid_controllers.get('linear', None)

    def initialize(self):
        self.finished = False

    def execute(self):
        if shared_data["distance"] < 10:
            self.end()
        else:
            speed = self.linear_pid.update(self.distance)
            self.chassis.translate(self.angle, speed)

    def end(self):
        self.finished = True
        self.chassis.stop()

    def isFinished(self):
        return self.finished
