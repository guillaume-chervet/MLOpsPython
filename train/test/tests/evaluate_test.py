import logging
import shutil
import unittest
from pathlib import Path

from integration import prepare_integration_data

BASE_PATH = Path(__file__).resolve().parent
output_directory = BASE_PATH / "output"
input_directory = BASE_PATH / "input"
input_model_directory = BASE_PATH / "input" / "model"
input_images_directory = BASE_PATH / "input" / "images"
input_integration_directory = BASE_PATH / "input" / "integration"


def execute(path:str):
    return {}

class EvaluateTest(unittest.TestCase):

    def test_prepare_integration_data(self):
        if output_directory.is_dir():
            shutil.rmtree(str(output_directory))
        output_directory.mkdir(parents=True, exist_ok=True)

        integration_output_directory = output_directory / "integration"
        integration_output_directory.mkdir(parents=True, exist_ok=True)
        prepare_integration_data(input_integration_directory, integration_output_directory, execute)

    #def test_evaluate(self):
    #    if output_directory.is_dir():
    #        shutil.rmtree(str(output_directory))
    #    output_directory.mkdir(parents=True, exist_ok=True)
    #    model_output_directory = output_directory / "model"
    #    model_output_directory.mkdir(parents=True, exist_ok=True)
    #    integration_output_directory = output_directory / "integration"
    #    integration_output_directory.mkdir(parents=True, exist_ok=True)
    #    execute_model_and_generate_integration_test_data(logging, input_model_directory, input_images_directory, input_integration_directory, model_output_directory, integration_output_directory)

if __name__ == '__main__':
    unittest.main()
