import unittest
from pathlib import Path
from unittest.mock import Mock

from mlopspython_extraction.extraction import ExtractImages, IDataManager, DataManager

BASE_PATH = Path(__file__).resolve().parent
output_directory = BASE_PATH / "output"
input_directory = BASE_PATH / "input"


class TestExtraction(unittest.TestCase):
    def test_pdfs_images_should_be_extracted(self):
        data_manager_mock = Mock(IDataManager)
        data_manager_mock.get_pdf_files = DataManager().get_pdf_files
        data_manager_mock.save_image = Mock()
        data_manager_mock.create_directory = Mock()

        extract_images = ExtractImages(data_manager_mock)

        input_directory_str = str(input_directory)
        output_directory_str = str(output_directory)
        extract_images.extract_images(input_directory_str, output_directory_str)

        data_manager_mock.create_directory.assert_called_once_with(output_directory_str)

        save_image_call = data_manager_mock.save_image.call_args_list
        self.assertTrue(save_image_call[0].args[1].endswith("a_page0_index0.png"))
        self.assertTrue(save_image_call[1].args[1].endswith("a_page1_index0.png"))
        self.assertTrue(save_image_call[2].args[1].endswith("b_page0_index0.png"))


if __name__ == "__main__":
    unittest.main()
