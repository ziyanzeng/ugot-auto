from ugot import ugot

class UGOTCamera:
    def __init__(self, ip):
        self.got = ugot.UGOT()
        self.ip = ip

    def open_camera(self):
        self.got.initialize(self.ip)
        self.got.open_camera()

    def read_camera_data(self):
        return self.got.read_camera_data()
