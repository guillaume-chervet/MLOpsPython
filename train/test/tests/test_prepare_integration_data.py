import shutil
from pathlib import Path
from integration import prepare_integration_data

BASE_PATH = Path(__file__).resolve().parent
output_directory = BASE_PATH / "output"
input_directory = BASE_PATH / "input"
input_integration_directory = input_directory / "integration"


def execute(_):
    return {}


def test_prepare_integration_data(tmp_path):
    if output_directory.is_dir():
        shutil.rmtree(str(output_directory))
    output_directory.mkdir(parents=True, exist_ok=True)

    integration_output_directory = output_directory / "integration"
    integration_output_directory.mkdir(parents=True, exist_ok=True)

    prepare_integration_data(input_integration_directory, integration_output_directory, execute)

    # Sanity check minimum: on a bien une arbo
    assert (integration_output_directory / "mlcli").exists()
