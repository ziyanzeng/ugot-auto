from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, got):
        self.got = got
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
