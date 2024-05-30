from .Command import Command
from .actuators.chassis import Chassis
from shared_data import SharedData

class AlignWithBallCommand(Command):
    def __init__(self, got):
        super().__init__(got)
        self.chassis = Chassis(got)
        self.angle_pid = SharedData.shared_data["angle_pid"]

    def initialize(self):
        self.finished = False

    def execute(self):
        if abs(SharedData.shared_data["angle"]) < 1:
            self.end()
        else:
            turn_speed = self.angle_pid.update(SharedData.shared_data["angle"])
            self.chassis.spin_on_location(turn_speed)

    def end(self):
        self.finished = True
        self.chassis.stop()

    def isFinished(self):
        return self.finished
