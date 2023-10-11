import json
from pathlib import Path


def prepare_integration_data(
    input_integration_directory, integration_output_directory, execute
):
    mlcli_directory = integration_output_directory / "mlcli"
    mlcli_directory.mkdir(parents=True, exist_ok=True)
    pdfs = [
        p
        for p in Path(input_integration_directory).iterdir()
        if p.is_file() and p.suffix == ".pdf"
    ]
    ground_truth_directory = integration_output_directory / "ground_truth"
    ground_truth_directory.mkdir(parents=True, exist_ok=True)
    for pdf_source_path in pdfs:
        destination_path = mlcli_directory / pdf_source_path.name
        destination_path.write_bytes(pdf_source_path.read_bytes())
        settings = {
            "data": [
                {"type": "file", "value": pdf_source_path.name},
                {"key": "type", "value": "pillow"},
            ]
        }
        with open(
            mlcli_directory / (pdf_source_path.stem + ".json"), "w"
        ) as file_stream:
            json.dump(settings, file_stream, indent=4)
    for pdf_source_path in pdfs:
        print("pdf_source_path: " + str(pdf_source_path))
        images_path = input_integration_directory / pdf_source_path.stem
        if not images_path.is_dir():
            print("images_path not exist: " + str(images_path))
            continue
        print("images_path: " + str(images_path))
        images = [
            p
            for p in images_path.iterdir()
            if p.is_file() and p.suffix == ".png"
        ]
        images.sort()
        responses = []
        for image_path in images:
            model_result = execute(str(image_path))
            responses.append(model_result)
        data = {
            "Url": "https://www.groundtruth.fr",
            "FileName": pdf_source_path.name,
            "FileDirectory": "",
            "ImageDirectory": "",
            "FrontDefaultStringsMatcher": "",
            "StatusCode": 200,
            "Body": json.dumps(responses),
            "Headers": [],
            "TimeMs": 0,
            "TicksAt": 0,
        }
        truth_filename = (
            Path(pdf_source_path).stem
            + "_"
            + Path(pdf_source_path).suffix.lower().replace(".", "")
            + ".json"
        )
        with open(ground_truth_directory / truth_filename, "w") as file_stream:
            json.dump(data, file_stream, indent=4)
