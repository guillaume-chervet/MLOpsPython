import shutil
import unittest
from pathlib import Path

from train import run_test_harness

BASE_PATH = Path(__file__).resolve().parent
output_directory = BASE_PATH / "output"
input_directory = BASE_PATH / "input"

class TrainTest(unittest.TestCase):

    def test_something(self):
        if output_directory.is_dir():
            shutil.rmtree(str(output_directory))
        model_result = run_test_harness(input_directory, output_directory)
        self.assertEqual(True, model_result.summary_image_path.is_file())
        self.assertEqual(True, model_result.model_path.is_file())


if __name__ == '__main__':
    unittest.main()
