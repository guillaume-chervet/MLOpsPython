import shutil
import unittest
from pathlib import Path
from unittest.mock import Mock

from label_split_data import DataSplit, LabelSplitDataInput, IDataRandom, DataRandom, IDataManager, DataManager

BASE_PATH = Path(__file__).resolve().parent
output_images_directory = BASE_PATH / "output_images"
output_pdf_directory = BASE_PATH / "output_integration"
input_directory = BASE_PATH / "input"
input_images_directory = input_directory / "images"
input_labels_path = input_directory / "labels" / "labels.json"
input_pdfs_directory = input_directory / "pdfs"


class LabelSplitDataTest(unittest.TestCase):
    def test_label_split_data(self):
        if output_images_directory.is_dir():
            shutil.rmtree(str(output_images_directory))
        if output_pdf_directory.is_dir():
            shutil.rmtree(str(output_pdf_directory))

        def shuffle(x):
            return x.reverse()

        data_ramdom_mock = Mock(DataRandom)
        data_ramdom_mock.shuffle = shuffle

        data_manager = DataManager()
        data_manager_mock = Mock(IDataManager)
        data_manager_mock.create_directory = Mock()
        data_manager_mock.copy_directory = Mock()
        data_manager_mock.copy_file = Mock()
        data_manager_mock.list_files = data_manager.list_files
        data_manager_mock.load_json = data_manager.load_json

        data_split = DataSplit(data_ramdom_mock, data_manager_mock)

        label_split_data_input = LabelSplitDataInput(
            input_labels_path,
            input_images_directory,
            input_pdfs_directory,
            output_images_directory,
            output_pdf_directory,
            number_image_by_label=3,
            number_pdfs_integration=1,
        )

        label_split_data_result = data_split.label_split_data(
            label_split_data_input
        )
        expected = ['train/cats/cat_b_page3_index0.png',
                    'test/cats/cat_b_page2_index0.png',
                    'evaluate/cats/cat_b_page1_index0.png',
                    'train/dogs/dog_c_page4_index0.png',
                    'test/dogs/dog_b_page4_index0.png',
                    'evaluate/dogs/dog_b_page2_index0.png',
                    'train/others/other_b_page1_index0.png',
                    'test/others/other_b_page2_index0.png',
                    'evaluate/others/other_a_page0_index0.png']


        for path_result in label_split_data_result.path_results:
            self.assertIn(path_result, expected)

        self.assertEqual(data_manager_mock.copy_file.call_count, 12)
        self.assertEqual(data_manager_mock.create_directory.call_count, 13)

        self.assertEqual(label_split_data_result.number_file_train_by_label, 1)
        self.assertEqual(label_split_data_result.number_file_test_by_label, 1)
        self.assertEqual(label_split_data_result.number_file_evaluate_by_label, 1)
        self.assertEqual(label_split_data_result.number_labeled_data, 9)


if __name__ == "__main__":
    unittest.main()
