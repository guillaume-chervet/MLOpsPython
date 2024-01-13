import shutil
import unittest
from pathlib import Path
from unittest.mock import MagicMock

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
            mypdf = None
            for c in x:
                if isinstance(c, Path) and str(c).endswith("c.pdf"):
                    mypdf = c
            if mypdf is not None:
                x.remove(mypdf)
                x.insert(0, mypdf)
            return x

        files_copied = []

        def copy_file(file_path: Path, to_file_path: Path) -> None:
            files_copied.append(str(to_file_path).replace(str(BASE_PATH), "").replace("\\", "/"))

        data_ramdom_mock = MagicMock(DataRandom)
        data_ramdom_mock.shuffle = shuffle

        data_manager = DataManager()
        data_manager_mock = MagicMock(IDataManager)
        data_manager_mock.create_directory = MagicMock()
        data_manager_mock.copy_file = copy_file
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
        expected = ['/output_integration/c.pdf',
                    '/output_integration/c/c_page4_index0.png',
                    '/output_images/train/cats/cat_b_page1_index0.png',
                    '/output_images/test/cats/cat_b_page2_index0.png',
                    '/output_images/evaluate/cats/cat_b_page3_index0.png',
                    '/output_images/train/dogs/dog_b_page2_index0.png',
                    '/output_images/test/dogs/dog_b_page4_index0.png',
                    '/output_images/train/others/other_a_page0_index0.png',
                    '/output_images/test/others/other_b_page2_index0.png',
                    '/output_images/evaluate/others/other_b_page1_index0.png']

        for path_result in files_copied:
            self.assertIn(path_result, expected)

        data_manager_mock.create_directory.assert_called()

        self.assertEqual(label_split_data_result.number_file_train_by_label, 1)
        self.assertEqual(label_split_data_result.number_file_test_by_label, 1)
        self.assertEqual(label_split_data_result.number_file_evaluate_by_label, 1)
        self.assertEqual(label_split_data_result.number_labeled_data, 9)


if __name__ == "__main__":
    unittest.main()
