from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, got, shared_data, pid_controllers=None):
        self.got = got
        self.shared_data = shared_data
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
