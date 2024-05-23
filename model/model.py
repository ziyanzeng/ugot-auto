from ultralytics import YOLO

class YOLOModel:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def predict(self, data):
        return self.model(data)
