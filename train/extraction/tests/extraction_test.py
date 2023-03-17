import shutil
import unittest
from pathlib import Path

from mlopspython_extraction.model_pillow import extract_images

BASE_PATH = Path(__file__).resolve().parent
output_directory = BASE_PATH / "output"
input_directory = BASE_PATH / "input"

class TestExtraction(unittest.TestCase):

    def test_pdfs_images_should_be_extracted(self):
        if output_directory.is_dir():
            shutil.rmtree(str(output_directory))
        result = extract_images(str(input_directory), str(output_directory))
        expected_number_files_input = 2
        self.assertEqual(result.number_files_input, expected_number_files_input)
        expected_number_images_output = 3
        self.assertEqual(result.number_images_output, expected_number_images_output)


if __name__ == "__main__":
    unittest.main()
