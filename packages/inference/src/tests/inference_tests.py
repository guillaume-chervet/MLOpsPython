import unittest
from pathlib import Path
import logging

from mlopspython_inference.model_pillow import Model

BASE_PATH = Path(__file__).resolve().parent
output_directory = BASE_PATH / "output"
input_directory = BASE_PATH / "input"

class TestInference(unittest.TestCase):

    def test_todo(self):
        model = Model(logging, str(input_directory / "model" / "final_model.h5"))
        model_result = model.execute(str(input_directory / "images" / "cat.png"))
        print(model_result)
        self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()
