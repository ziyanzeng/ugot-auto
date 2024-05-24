from .LocateBallCommand import LocateBallCommand
from .TranslateToBallCommand import TranslateToBallCommand
from .AlignWithBallCommand import AlignWithBallCommand

class CommandPlanner:
    def __init__(self, got, shared_data, pid_controllers):
        self.got = got
        self.shared_data = shared_data
        self.pid_controllers = pid_controllers
        self.current_command = None

    def update(self, distance, angle):
        with self.shared_data["lock"]:
            if self.shared_data["detections"] is None:
                if not isinstance(self.current_command, LocateBallCommand):
                    self.current_command = LocateBallCommand(self.got, self.shared_data, self.pid_controllers)
                    self.current_command.initialize()
            elif distance >= 10:
                if not isinstance(self.current_command, TranslateToBallCommand):
                    self.current_command = TranslateToBallCommand(self.got, self.shared_data, distance, angle, self.pid_controllers)
                    self.current_command.initialize()
            elif distance < 10 and abs(angle) >= 1:
                if not isinstance(self.current_command, AlignWithBallCommand):
                    self.current_command = AlignWithBallCommand(self.got, self.shared_data, angle, self.pid_controllers)
                    self.current_command.initialize()

            if self.current_command is not None:
                self.current_command.execute()
                if self.current_command.isFinished():
                    self.current_command.end()
                    self.current_command = None
