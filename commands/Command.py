from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, got, pid_controllers=None):
        self.got = got
        self.pid_controllers = pid_controllers if pid_controllers is not None else {}
        self.finished = False

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def end(self):
        pass
    
    @abstractmethod
    def isFinished(self):
        pass
