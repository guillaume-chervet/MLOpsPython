import argparse
from pathlib import Path

parser = argparse.ArgumentParser("output")
parser.add_argument("--extraction_images_input", type=str)
parser.add_argument("--extraction_hash_input", type=str)
parser.add_argument("--model_input", type=str)
parser.add_argument("--integration_input", type=str)
parser.add_argument("--main_output", type=str)

args = parser.parse_args()
extraction_images_input = args.extraction_images_input
extraction_hash_input = args.extraction_hash_input
model_input = args.model_input
integration_input = args.integration_input
main_output = args.main_output


def copy_files(input_path: str, output_path: str):
    path_source = Path(input_path)
    path_destination = Path(output_path)

    path_destination.mkdir(parents=True, exist_ok=True)

    for file in path_source.glob("*"):
        if file.is_file():
            with file.open("rb") as f_source:
                content = f_source.read()
            with (path_destination / file.name).open("wb") as f_destination:
                f_destination.write(content)


copy_files(extraction_images_input, str(Path(main_output) / "extraction_images"))
copy_files(extraction_hash_input, str(Path(main_output) / "extraction_hash"))
copy_files(model_input, str(Path(main_output) / "model"))
copy_files(integration_input, str(Path(main_output) / "integration"))
