import logging
import shutil
import unittest
from pathlib import Path

from evaluate import evaluate

BASE_PATH = Path(__file__).resolve().parent
output_directory = BASE_PATH / "output"
input_directory = BASE_PATH / "input"


class EvaluateTest(unittest.TestCase):

    def tearDown(self):
        if output_directory.is_dir():
            shutil.rmtree(str(output_directory))

    def test_evaluate(self):
        output_directory.mkdir(parents=True, exist_ok=True)
        model_output_directory = output_directory / "model"
        model_output_directory.mkdir(parents=True, exist_ok=True)
        integration_output_directory = output_directory / "integration"
        integration_output_directory.mkdir(parents=True, exist_ok=True)
        evaluate(logging, input_directory, model_output_directory, integration_output_directory)

if __name__ == '__main__':
    unittest.main()
