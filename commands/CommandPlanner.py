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

    def update(self):
        # logger.info(f'Update called with distance: {distance}, angle: {angle}')

        self.prev_command = self.current_command
        # logger.info('Planning next command...')
        if SharedData.shared_data["detections"] is None or (SharedData.shared_data["distance"] == 0 and SharedData.shared_data["angle"] == 0):
            if self.current_command != "locate":
                logger.info('Switching to LocateBallCommand')
                self.current_command = "locate"
                SharedData.shared_data["command"] = "locate"
        elif SharedData.shared_data["distance"] >= 15:
            if self.current_command != "translate":
                logger.info(f'Switching to TranslateToBallCommand with distance: {SharedData.shared_data["distance"]}, angle: {SharedData.shared_data["angle"]}')
                self.current_command = "translate"
                SharedData.shared_data["command"] = "translate"
        elif SharedData.shared_data["distance"] < 15 and abs(SharedData.shared_data["angle"]) >= 1:
            if self.current_command != "align":
                logger.info(f'Switching to AlignWithBallCommand with angle: {SharedData.shared_data["angle"]}')
                self.current_command = "align"
                SharedData.shared_data["command"] = "align"
        else:
            if self.current_command == "rest": return
            self.current_command = "rest"
            SharedData.shared_data["command"] = "rest"
        # logger.info('Command Planner Update completed')
