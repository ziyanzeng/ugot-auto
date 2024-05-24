import unittest
from commands.LocateBallCommand import LocateBallCommand
from commands.TranslateToBallCommand import TranslateToBallCommand
from commands.AlignWithBallCommand import AlignWithBallCommand
from commands.CommandPlanner import CommandPlanner
from ugot import ugot
import config
import utils

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.got = ugot.UGOT()
        self.pid_controllers = {
            "linear": utils.PID(kp=0.1, ki=0.01, kd=0.05),
            "angle": utils.PID(kp=0.1, ki=0.01, kd=0.05)
        }

    def test_locate_ball_command(self):
        command = LocateBallCommand(self.got, config.shared_data, self.pid_controllers)
        command.initialize()
        self.assertFalse(command.isFinished())
        command.execute()
        self.assertFalse(command.isFinished())

    def test_translate_to_ball_command(self):
        command = TranslateToBallCommand(self.got, config.shared_data, 15, 0, self.pid_controllers)
        command.initialize()
        self.assertFalse(command.isFinished())
        command.execute()
        self.assertFalse(command.isFinished())

    def test_align_with_ball_command(self):
        command = AlignWithBallCommand(self.got, config.shared_data, 10, self.pid_controllers)
        command.initialize()
        self.assertFalse(command.isFinished())
        command.execute()
        self.assertFalse(command.isFinished())

if __name__ == '__main__':
    unittest.main()
