from ugot import ugot

class UGOTCamera:
    def __init__(self, got):
        self.got = got

    def open_camera(self):
        self.got.open_camera()

    def read_camera_data(self):
        return self.got.read_camera_data()
    
    def close_camera(self):
        self.got.close_camera()
