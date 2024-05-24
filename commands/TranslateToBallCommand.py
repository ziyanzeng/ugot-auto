from .Command import Command
from .actuators.chassis import Chassis

class TranslateToBallCommand(Command):
    def __init__(self, got, shared_data, distance, angle, pid_controllers=None):
        super().__init__(got, shared_data, pid_controllers)
        self.chassis = Chassis(got)
        self.distance = distance
        self.angle = angle

    def initialize(self):
        self.finished = False

    def execute(self):
        with self.shared_data["lock"]:
            if self.distance < 10:
                self.finished = True
                self.chassis.stop()
            else:
                self.chassis.translate(self.angle, 20)

    def end(self):
        self.chassis.stop()

    def isFinished(self):
        return self.finished
