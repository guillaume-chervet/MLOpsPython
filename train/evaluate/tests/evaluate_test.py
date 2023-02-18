import logging
import shutil
import unittest
from pathlib import Path

from evaluate import evaluate

BASE_PATH = Path(__file__).resolve().parent
output_directory = BASE_PATH / "output"
input_directory = BASE_PATH / "input"
input_model_directory = BASE_PATH / "input" / "model"
input_images_directory = BASE_PATH / "input" / "images"


class EvaluateTest(unittest.TestCase):

    def test_evaluate(self):
        if output_directory.is_dir():
            shutil.rmtree(str(output_directory))
        output_directory.mkdir(parents=True, exist_ok=True)
        model_output_directory = output_directory / "model"
        model_output_directory.mkdir(parents=True, exist_ok=True)
        integration_output_directory = output_directory / "integration"
        integration_output_directory.mkdir(parents=True, exist_ok=True)
        evaluate(logging, input_model_directory, input_images_directory, model_output_directory, integration_output_directory)

if __name__ == '__main__':
    unittest.main()
