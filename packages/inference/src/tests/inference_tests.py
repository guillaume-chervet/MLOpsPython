import unittest
from pathlib import Path
import logging

from mlopspython_inference.model_pillow import Model

BASE_PATH = Path(__file__).resolve().parent
output_directory = BASE_PATH / "output"
input_directory = BASE_PATH / "input"

class TestInference(unittest.TestCase):

    def test_inference(self):
        model = Model(logging, str(input_directory / "model" / "final_model.h5"))
        inference_result = model.execute(str(input_directory / "images" / "cat.png"))

        expected_result = {'prediction': 'Cat', 'values': [1.0, 2.370240289845506e-30, 0.0]}
        self.assertEqual(inference_result, expected_result)


if __name__ == "__main__":
    unittest.main()
