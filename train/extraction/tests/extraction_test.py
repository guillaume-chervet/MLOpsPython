import shutil
import unittest
from pathlib import Path

from extraction import extract_images

BASE_PATH = Path(__file__).resolve().parent


class TestExtraction(unittest.TestCase):
    output_directory = BASE_PATH / 'output'
    input_directory = BASE_PATH / 'input'

    def tearDown(self):
       if self.output_directory.is_dir():
           shutil.rmtree(str(self.output_directory))

    def test_pdfs_images_should_be_extracted(self):
        extract_images(str(self.input_directory), str(self.output_directory))
        images = [p for p in Path(self.output_directory).iterdir() if p.is_file()]
        expected = 3
        self.assertEqual(len(images), expected)

if __name__ == '__main__':
    unittest.main()
