import shutil
import unittest
from pathlib import Path

from label_split_data import label_split_data

BASE_PATH = Path(__file__).resolve().parent


class LabelSplitDataTest(unittest.TestCase):
    output_directory = BASE_PATH / "output"
    input_directory = BASE_PATH / "input"
    input_images_directory = input_directory / "images"
    input_labels_path = input_directory / "labels" / "labels.json"

    def tearDown(self):
        if self.output_directory.is_dir():
            shutil.rmtree(str(self.output_directory))

    def test_label_split_data(self):

        path_results = label_split_data(self.input_labels_path, self.input_images_directory, self.output_directory)
        expected = ['train/cats/cat_0a2bc279-8a6b-49fd-9857-d047351cd5e1_page1_index0.png',
                    'test/cats/cat_0a2bc279-8a6b-49fd-9857-d047351cd5e9_page1_index0.png',
                    'evaluate/cats/cat_0a2bc279-8a6b-49fd-9857-d047351cd5e9_page3_index0.png',
                    'train/dogs/dog_0a2bc279-8a6b-49fd-9857-d047351cd5e9_page2_index0.png',
                    'test/dogs/dog_0a2bc279-8a6b-49fd-9857-d047351cd5e9_page4_index0.png',
                    'evaluate/dogs/dog_0a2bc279-8a6b-49fd-9857-d047351cd5e10_page4_index0.png',
                    'train/others/other_0a0e5d35-ef01-4239-af60-81f2357a6ab9_page0_index0.png',
                    'test/others/other_0a0e5d35-ef01-4239-af60-81f2357a6ab9_page2_index0.png',
                    'evaluate/others/other_0a0e5d35-ef01-4239-af60-81f2357a6ab9_page1_index0.png']
        for path_result in path_results:
            self.assertIn(path_result, expected)


if __name__ == '__main__':
    unittest.main()
