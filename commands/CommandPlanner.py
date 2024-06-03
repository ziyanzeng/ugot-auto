from .LocateBallCommand import LocateBallCommand
from .TranslateToBallCommand import TranslateToBallCommand
from .AlignWithBallCommand import AlignWithBallCommand
from .RestCommand import RestCommand
from shared_data import SharedData
from logger import logger

class CommandPlanner:
    def __init__(self, got):
        self.got = got
        self.current_command = LocateBallCommand(self.got)
        logger.info('CommandPlanner initiated')
        self.prev_command = None

    def update(self):
        # logger.info(f'Update called with distance: {distance}, angle: {angle}')

        if self.current_command.isFinished():
            self.prev_command = self.current_command
            # logger.info('Planning next command...')
            if SharedData.shared_data["detections"] is None or (SharedData.shared_data["distance"] == 0 and SharedData.shared_data["angle"] == 0):
                if not isinstance(self.current_command, LocateBallCommand):
                    logger.info('Switching to LocateBallCommand')
                    self.current_command = LocateBallCommand(self.got)
                    self.current_command.initialize()
            elif SharedData.shared_data["distance"] >= 15:
                if not isinstance(self.current_command, TranslateToBallCommand):
                    logger.info(f'Switching to TranslateToBallCommand with distance: {SharedData.shared_data["distance"]}, angle: {SharedData.shared_data["angle"]}')
                    self.current_command = TranslateToBallCommand(self.got)
                    self.current_command.initialize()
            elif SharedData.shared_data["distance"] < 15 and abs(SharedData.shared_data["angle"]) >= 1:
                if not isinstance(self.current_command, AlignWithBallCommand):
                    logger.info(f'Switching to AlignWithBallCommand with angle: {SharedData.shared_data["angle"]}')
                    self.current_command = AlignWithBallCommand(self.got)
                    self.current_command.initialize()
            else:
                if isinstance(self.current_command, RestCommand): return
                self.current_command = RestCommand(self.got)
                self.current_command.initialize()
            # logger.info('Command updated')

        if self.current_command is not None:
            if type(self.current_command).__name__ != type(self.prev_command).__name__: 
                logger.info(f'Executing command: {type(self.current_command).__name__}')
            self.current_command.execute()
            if self.current_command.isFinished():
                logger.info(f'Command {type(self.current_command).__name__} is finished')
        # logger.info('Command Planner Update completed')
        
        return type(self.current_command).__name__ 
