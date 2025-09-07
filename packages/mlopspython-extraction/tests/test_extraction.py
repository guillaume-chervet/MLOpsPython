from pathlib import Path
from unittest.mock import Mock

from mlopspython_extraction.extraction import ExtractImages, IDataManager, DataManager

BASE_PATH = Path(__file__).resolve().parent
output_directory = BASE_PATH / "output"
input_directory = BASE_PATH / "input"


def test_pdfs_images_should_be_extracted(tmp_path):
    data_manager_mock = Mock(IDataManager)
    # on utilise la vraie implémentation pour lister les PDF
    data_manager_mock.get_pdf_files = DataManager().get_pdf_files
    data_manager_mock.save_image = Mock()
    data_manager_mock.create_directory = Mock()

    extract_images = ExtractImages(data_manager_mock)

    input_directory_str = str(input_directory)
    output_directory_str = str(tmp_path / "out")
    extract_images.extract_images(input_directory_str, output_directory_str)

    data_manager_mock.create_directory.assert_called_once_with(output_directory_str)

    calls = data_manager_mock.save_image.call_args_list
    # vérifie les 3 premières écritures attendues
    assert calls[0].args[1].endswith("a_page0_index0.png")
    assert calls[1].args[1].endswith("a_page1_index0.png")
    assert calls[2].args[1].endswith("b_page0_index0.png")
