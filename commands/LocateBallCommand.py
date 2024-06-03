from .Command import Command
from .actuators.chassis import Chassis
from shared_data import SharedData
from logger import logger

class LocateBallCommand(Command):
    def __init__(self, got):
        super().__init__(got)
        self.chassis = Chassis(got)
        self.cummulate = 0

    def initialize(self):
        self.finished = False

    def execute(self):
        self.cummulate += 1
        # end only when target is found
        if SharedData.shared_data["angle"] != 0 and SharedData.shared_data["distance"] != 0 or self.cummulate > 1000:
            self.end()
        else:
            turn_speed = 75
            self.chassis.spin_on_location(turn_speed)

    def end(self):
        self.finished = True
        self.chassis.stop()

    def isFinished(self):
        return self.finished
