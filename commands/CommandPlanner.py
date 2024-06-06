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
        self.prev_command = "rest"

    def update(self, update_signal):
        # logger.info(f'Update called with distance: {distance}, angle: {angle}')
        if self.prev_command == "kick":
            if not SharedData.shared_data["restart_trial"]:
                logger.info("Current trial ended, waiting for next trial signal...")
                return
            else:
                logger.info("New trial signal received from web panel! Running next command trial!")
                SharedData.shared_data["restart_trial"] = False
        # logger.info('Planning next command...')
        if update_signal:
            # distance = SharedData.shared_data["distance"]
            # angle = SharedData.shared_data["angle"]
            # logger.info(f"data received in command planner: distance - {distance}, angel - {angle}")
            if SharedData.shared_data["detections"] is None or (SharedData.shared_data["distance"] == 0 and SharedData.shared_data["angle"] == 0):
                logger.info('Switching to LocateBallCommand')
                self.current_command = "locate"
                SharedData.shared_data["command"] = self.current_command
            elif abs(SharedData.shared_data["angle"]) >= 1:
                logger.info('aligning...')
                self.current_command = "align"
                SharedData.shared_data["command"] = self.current_command
            elif SharedData.shared_data["distance"] >= 15:
                logger.info(f'Switching to TranslateToBallCommand with distance: {SharedData.shared_data["distance"]}, angle: {SharedData.shared_data["angle"]}')
                self.current_command = "translate"
                SharedData.shared_data["command"] = self.current_command
            elif SharedData.shared_data["distance"] < 15 and abs(SharedData.shared_data["angle"]) <= 5 and self.prev_command != "goal":
                logger.info("switching to goal aimming command")
                self.current_command = "goal"
                SharedData.shared_data["command"] = self.current_command
            elif self.prev_command == "goal" or self.prev_command == "align":
                if abs(SharedData.shared_data["angle"]) >= 3:
                    logger.info("final stage alinging before kick")
                    self.current_command = "align"
                    SharedData.shared_data["command"] = self.current_command
                elif self.prev_command != "kick":
                    logger.info("switching to kick command")
                    self.current_command = "kick"
                    SharedData.shared_data["command"] = self.current_command
            else:
                logger.info("branching to rest command, robot in idle mode")
                # if self.prev_command == "rest": return
                self.current_command = "rest"
                SharedData.shared_data["command"] = self.current_command
                
            self.prev_command = self.current_command
        # logger.info('Command Planner Update completed')
        return
