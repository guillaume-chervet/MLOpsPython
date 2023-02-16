import logging
import unittest
from pathlib import Path

from model_pillow import Model

BASE_PATH = Path(__file__).resolve().parent
output_directory = BASE_PATH / "output"
input_directory = BASE_PATH / "input"

class EvaluateTest(unittest.TestCase):

    def test_something(self):

        model = Model(logging, str(input_directory / "final_model.h5"))

        cats_directory = input_directory / "evaluate" / "cats"
        for path in cats_directory.glob("*"):
            model_result = model.execute(str(path))
            print(model_result)




if __name__ == '__main__':
    unittest.main()
