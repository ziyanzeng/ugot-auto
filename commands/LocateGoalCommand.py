from .Command import Command
from .actuators.chassis import Chassis
from shared_data import SharedData
from logger import logger
from utils.pid_controller import PID
import config

class LocateGoalCommand(Command):
    def __init__(self, got):
        super().__init__(got)
        self.chassis = Chassis(got)
        self.cummulate = 0
        # self.pivot_pid = PID(config.PIVOT_KP, config.PIVOT_KI, config.PIVOT_KD)
        self.pivot_pid = PID(config.PIVOT_KP, config.PIVOT_KI, config.PIVOT_KD)
        self.align_pid = PID(config.LINEAR_KP, config.LINEAR_KI, config.LINEAR_KD)
        self.linear_pid = PID(config.LINEAR_KP, config.LINEAR_KI, config.LINEAR_KD)

    def initialize(self):
        self.finished = False
        logger.info("locate goal command initialized")

    def execute(self):
        self.cummulate += 1
        # end only when target is found and locked
        logger.info("goal angle: " + str(SharedData.shared_data["angle_goal"]))
        distance_to_ball = SharedData.shared_data["distance"]
        angle_to_ball = SharedData.shared_data["angle"]
        if distance_to_ball == 0:
            return
        elif SharedData.shared_data["angle_goal"] != 0 and SharedData.shared_data["distance_goal"] != 0 or self.cummulate > 1000:
            logger.info("goal located")
            if abs(SharedData.shared_data["angle_goal"]) > 1:
                logger.info("locking goal")
                velocity = min((self.pivot_pid.update(abs(SharedData.shared_data["angle_goal"]))), 40)
                logger.info("pivot drifting velocity: " + str(velocity))
                self.chassis.turn_on_pivot(distance_to_ball, -1 * SharedData.shared_data["angle_goal"] / abs(SharedData.shared_data["angle_goal"]), velocity)
            elif abs(angle_to_ball) > 1:
                logger.info("aligning in locking goal command")
                align_speed = min(self.align_pid.update(angle_to_ball), 40)
                self.chassis.translate(90 if angle_to_ball > 0 else -90, align_speed)
                if abs(angle_to_ball) <= 1: self.align_pid.reset_integral()
            elif abs(distance_to_ball - 12) > 1:
                logger.info("distance adjusting in locking goal command")
                error = distance_to_ball - 12
                linear_speed = min(self.linear_pid.update(abs(error)), 40)
                logger.info("linear speed: " + str(linear_speed))
                self.chassis.translate(0 if error > 0 else -180, linear_speed)
                if abs(distance_to_ball - 12) <= 1: self.linear_pid.reset_integral()
            else:
                logger.info("goal locked")
                self.end()
        else:
            logger.info("searching for goal...")
            self.chassis.turn_on_pivot(SharedData.shared_data["distance"], -1, 15)

    def end(self):
        self.finished = True
        self.chassis.stop()

    def isFinished(self):
        return self.finished
