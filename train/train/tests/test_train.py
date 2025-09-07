from pathlib import Path
import shutil
import pytest

from train import run_test_harness

BASE_PATH = Path(__file__).resolve().parent
output_directory = BASE_PATH / "output"
input_directory = BASE_PATH / "input"


@pytest.mark.skip(reason="Test lourd (TensorFlow). Retire ce skip si tu veux l'exécuter en CI.")
def test_run_test_harness_creates_artifacts():
    if output_directory.is_dir():
        shutil.rmtree(str(output_directory))
    result = run_test_harness(input_directory, output_directory, epochs=1)
    assert result.summary_image_path.is_file()
    assert result.model_path.is_file()
