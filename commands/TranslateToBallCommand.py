from .Command import Command
from .actuators.chassis import Chassis
from config import shared_data
from logger import logger

class TranslateToBallCommand(Command):
    def __init__(self, got, pid_controllers=None):
        super().__init__(got, pid_controllers)
        self.chassis = Chassis(got)
        self.linear_pid = self.pid_controllers.get('linear', None)

    def initialize(self):
        self.finished = False

    def execute(self):
        # end if move finished or target lost
        # logger.info(f'shared data: distance - {shared_data["distance"]}, angle: {shared_data["angle"]}')
        if shared_data["distance"] < 10 or (shared_data["detections"] is None and (shared_data["angle"] == 0 or shared_data["distance"] == 0)):
            self.end()
        else:
            speed = self.linear_pid.update(shared_data["distance"])
            self.chassis.translate(shared_data["angle"], speed)

    def end(self):
        self.finished = True
        self.chassis.stop()

    def isFinished(self):
        return self.finished
