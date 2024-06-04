from .Command import Command
from .actuators.chassis import Chassis
from shared_data import SharedData
from logger import logger
from utils.pid_controller import PID
import config

class TranslateToBallCommand(Command):
    def __init__(self, got):
        super().__init__(got)
        self.chassis = Chassis(got)
        self.linear_pid = PID(config.LINEAR_KP, config.LINEAR_KI, config.LINEAR_KD)

    def initialize(self):
        self.finished = False

    def execute(self):
        # end if move finished or target lost
        # logger.info(f'shared data: distance - {shared_data["distance"]}, angle: {shared_data["angle"]}')
        if SharedData.shared_data["distance"] < 15 or (SharedData.shared_data["detections"] is None and (SharedData.shared_data["angle"] == 0 or SharedData.shared_data["distance"] == 0)):
            self.end()
        else:
            speed = self.linear_pid.update(SharedData.shared_data["distance"])
            self.chassis.translate(SharedData.shared_data["angle"], speed)

    def end(self):
        self.finished = True
        self.chassis.stop()

    def isFinished(self):
        return self.finished
