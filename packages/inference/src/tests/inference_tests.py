import shutil
import unittest
from pathlib import Path

#from mlopspython_extraction.extraction import extract_images

BASE_PATH = Path(__file__).resolve().parent
output_directory = BASE_PATH / "output"
input_directory = BASE_PATH / "input"

class TestInference(unittest.TestCase):

    def test_todo(self):

        self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()
