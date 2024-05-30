from .Command import Command

class ArmRestoreCommand(Command):
    def __init__(self, got):
        self.got = got