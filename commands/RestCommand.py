from .Command import Command
from .actuators.chassis import Chassis
from config import shared_data
from logger import logger

class RestCommand(Command):
    def __init__(self, got):
        self.chassis = Chassis(got)

    def initialize(self):
        self.finished = False
        
    def execute(self):
        self.chassis.stop()
        self.end()
        
    def end(self):
        self.finished = True

    def isFinished(self):
        return self.finished