import shutil
import unittest
from pathlib import Path

from label_split_data import label_split_data

BASE_PATH = Path(__file__).resolve().parent
output_directory = BASE_PATH / "output"
input_directory = BASE_PATH / "input"
input_images_directory = input_directory / "images"
input_labels_path = input_directory / "labels" / "labels.json"

class LabelSplitDataTest(unittest.TestCase):

    def test_label_split_data(self):
        if output_directory.is_dir():
            shutil.rmtree(str(output_directory))
        label_split_data_result = label_split_data(input_labels_path, input_images_directory, output_directory)
        expected = ['train/cats/cat_0a2bc279-8a6b-49fd-9857-d047351cd5e1_page1_index0.png',
                    'test/cats/cat_0a2bc279-8a6b-49fd-9857-d047351cd5e9_page1_index0.png',
                    'evaluate/cats/cat_0a2bc279-8a6b-49fd-9857-d047351cd5e9_page3_index0.png',
                    'train/dogs/dog_0a2bc279-8a6b-49fd-9857-d047351cd5e9_page2_index0.png',
                    'test/dogs/dog_0a2bc279-8a6b-49fd-9857-d047351cd5e9_page4_index0.png',
                    'evaluate/dogs/dog_0a2bc279-8a6b-49fd-9857-d047351cd5e10_page4_index0.png',
                    'train/others/other_0a0e5d35-ef01-4239-af60-81f2357a6ab9_page0_index0.png',
                    'test/others/other_0a0e5d35-ef01-4239-af60-81f2357a6ab9_page2_index0.png',
                    'evaluate/others/other_0a0e5d35-ef01-4239-af60-81f2357a6ab9_page1_index0.png']
        for path_result in label_split_data_result.path_results:
            self.assertIn(path_result, expected)
        self.assertEqual(label_split_data_result.number_file_train_by_label, 1)
        self.assertEqual(label_split_data_result.number_file_test_by_label, 1)
        self.assertEqual(label_split_data_result.number_file_evaluate_by_label, 1)


if __name__ == '__main__':
    unittest.main()
