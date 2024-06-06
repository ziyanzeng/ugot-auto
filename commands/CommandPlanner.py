from .LocateBallCommand import LocateBallCommand
from .TranslateToBallCommand import TranslateToBallCommand
from .AlignWithBallCommand import AlignWithBallCommand
from .RestCommand import RestCommand
from shared_data import SharedData
from logger import logger

class CommandPlanner:
    def __init__(self, got):
        self.got = got
        self.current_command = "locate"
        logger.info('CommandPlanner initiated')
        self.prev_command = None

    def update(self, update_signal):
        # logger.info(f'Update called with distance: {distance}, angle: {angle}')
        if self.prev_command == "kick":
            return
        # logger.info('Planning next command...')
        if update_signal:
            if SharedData.shared_data["detections"] is None or (SharedData.shared_data["distance"] == 0 and SharedData.shared_data["angle"] == 0):
                if self.prev_command != "locate":
                    logger.info('Switching to LocateBallCommand')
                    self.current_command = "locate"
                    SharedData.shared_data["command"] = self.current_command
            elif SharedData.shared_data["angle"] >= 1:
                if self.prev_command != "align" and self.prev_command == "locate":
                    logger.info('aligning on ball after locating')
                    self.current_command = "align"
                    SharedData.shared_data["command"] = self.current_command
                elif self.prev_command != "align" and self.prev_command == "translate":
                    logger.info('aligning before locking on goal')
                    self.current_command = "align"
                    SharedData.shared_data["command"] = self.current_command
            elif SharedData.shared_data["distance"] >= 12:
                if self.prev_command != "translate" and self.prev_command == "align":
                    logger.info(f'Switching to TranslateToBallCommand with distance: {SharedData.shared_data["distance"]}, angle: {SharedData.shared_data["angle"]}')
                    self.current_command = "translate"
                    SharedData.shared_data["command"] = self.current_command
            elif SharedData.shared_data["distance"] < 15 and abs(SharedData.shared_data["angle"]) <= 1:
                if self.prev_command != "goal":
                    logger.info("switching to goal aimming command")
                    self.current_command = "goal"
                    SharedData.shared_data["command"] = self.current_command
            elif SharedData.shared_data["distance"] <= 12 and SharedData.shared_data["angle"] <= 1 and SharedData.shared_data["angle_goal"] <= 1:
                if self.prev_command != "kick":
                    logger.info("switching to kick command")
                    self.current_command = "kick"
                    SharedData.shared_data["command"] = self.current_command
            else:
                logger.info("branching to rest command, robot in idle mode")
                if self.prev_command == "rest": return
                self.current_command = "rest"
                SharedData.shared_data["command"] = self.current_command
                
            self.prev_command = self.current_command
        # logger.info('Command Planner Update completed')
        return
