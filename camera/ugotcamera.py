from ugot import ugot
from logger import logger

class UGOTCamera:
    def __init__(self, got):
        self.got = got

    def open_camera(self):
        self.got.open_camera()
        logger.info('camera opened')
        return True

    def read_camera_data(self):
        # logger.info('reading camera data')
        return self.got.read_camera_data()
    
    def close_camera(self):
        # self.got.close_camera()
        return True
