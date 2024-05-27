from .LocateBallCommand import LocateBallCommand
from .TranslateToBallCommand import TranslateToBallCommand
from .AlignWithBallCommand import AlignWithBallCommand
from config import shared_data
from logger import logger

class CommandPlanner:
    def __init__(self, got, pid_controllers):
        self.got = got
        self.pid_controllers = pid_controllers
        self.current_command = LocateBallCommand(self.got, self.pid_controllers)
        logger.info('CommandPlanner initiated')

    def update(self, distance, angle):
        logger.info(f'Update called with distance: {distance}, angle: {angle}')
        
        # Example of logging each step
        logger.info('Starting command planning')

        if self.current_command.isFinished():
            if shared_data["detections"] is None:
                if not isinstance(self.current_command, LocateBallCommand):
                    logger.info('Switching to LocateBallCommand')
                    self.current_command = LocateBallCommand(self.got, self.pid_controllers)
                    self.current_command.initialize()
            elif distance >= 10:
                if not isinstance(self.current_command, TranslateToBallCommand):
                    logger.info(f'Switching to TranslateToBallCommand with distance: {distance}, angle: {angle}')
                    self.current_command = TranslateToBallCommand(self.got, self.pid_controllers)
                    self.current_command.initialize()
            elif distance < 10 and abs(angle) >= 1:
                if not isinstance(self.current_command, AlignWithBallCommand):
                    logger.info(f'Switching to AlignWithBallCommand with angle: {angle}')
                    self.current_command = AlignWithBallCommand(self.got, self.pid_controllers)
                    self.current_command.initialize()

        logger.info('Command updated')

        if self.current_command is not None:
            logger.info(f'Executing command: {type(self.current_command).__name__}')
            self.current_command.execute()
            if self.current_command.isFinished():
                logger.info(f'Command {type(self.current_command).__name__} finished')
        logger.info('Update completed')
