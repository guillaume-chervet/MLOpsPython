import shutil
import unittest
from pathlib import Path

from extraction import extract_images

BASE_PATH = Path(__file__).resolve().parent


class TestExtraction(unittest.TestCase):
    output_directory = BASE_PATH / "output"
    input_directory = BASE_PATH / "input"

    def tearDown(self):
        if self.output_directory.is_dir():
            shutil.rmtree(str(self.output_directory))

    def test_pdfs_images_should_be_extracted(self):
        result = extract_images(str(self.input_directory), str(self.output_directory))
        expected_number_files_input = 2
        self.assertEqual(result.number_files_input, expected_number_files_input)
        expected_number_images_output = 3
        self.assertEqual(result.number_images_output, expected_number_images_output)


if __name__ == "__main__":
    unittest.main()
