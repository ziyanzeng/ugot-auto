from .Command import Command
from .actuators.chassis import Chassis
from shared_data import SharedData
from logger import logger

class LocateGoalCommand(Command):
    def __init__(self, got):
        super().__init__(got)
        self.chassis = Chassis(got)
        self.cummulate = 0

    def initialize(self):
        self.finished = False
        logger.info("locate goal command initialized")

    def execute(self):
        self.cummulate += 1
        # end only when target is found and locked
        logger.info("goal angle: " + str(SharedData.shared_data["angle_goal"]))
        if SharedData.shared_data["angle_goal"] != 0 and SharedData.shared_data["distance_goal"] != 0 or self.cummulate > 1000:
            logger.info("goal located")
            if abs(SharedData.shared_data["angle_goal"]) > 1 and SharedData.shared_data["distance"] != 0:
                logger.info("locking goal")
                self.chassis.turn_on_pivot(SharedData.shared_data["distance"], -1 * SharedData.shared_data["angle_goal"] / abs(SharedData.shared_data["angle_goal"]))
            else:
                logger.info("goal locked")
                self.end()
        else:
            logger.info("searching for goal...")
            self.chassis.turn_on_pivot(SharedData.shared_data["distance"], -1)

    def end(self):
        self.finished = True
        self.chassis.stop()

    def isFinished(self):
        return self.finished
