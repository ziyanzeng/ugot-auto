import unittest
from model import YOLOModel
import numpy as np

class TestYOLOModel(unittest.TestCase):
    def setUp(self):
        self.model = YOLOModel('./model/ball.pt')

    def test_model_initialization(self):
        self.assertIsNotNone(self.model)

    def test_model_prediction(self):
        # Create a dummy image (replace with actual test data if available)
        dummy_image = np.zeros((480, 640, 3), dtype=np.uint8)
        results = self.model.predict(dummy_image)
        self.assertIsNotNone(results)

if __name__ == '__main__':
    unittest.main()
