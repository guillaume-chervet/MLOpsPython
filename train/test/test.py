import json
from pathlib import Path

from mlopspython_inference.inference_pillow import Inference

model_name = "final_model.keras"


def execute_model_and_generate_integration_test_data(
    logging,
    input_model_directory: Path,
    input_images_directory: Path,
    input_integration_directory: Path,
    model_output_directory: Path,
    integration_output_directory: Path,
):
    model_path = input_model_directory / model_name
    model = Inference(logging, str(model_path))

    statistics = {"ok": 0, "ko": 0, "total": 0}
    results = []
    tests_directory = input_images_directory / "test"
    for path in tests_directory.glob("**/*"):
        if path.is_dir():
            continue
        model_result = model.execute(str(path))

        prediction = model_result["prediction"]
        prediction_truth = path.parent.name.lower().replace("s", "")
        status = prediction_truth == prediction.lower()
        statistics["ok" if status else "ko"] += 1
        result = {
            "filename": path.name,
            "ok": status,
            "prediction": prediction,
            "prediction_truth": prediction_truth,
            "values": model_result["values"],
        }
        results.append(result)
    statistics["total"] = statistics["ok"] + statistics["ko"]

    with open(model_output_directory / "statistics.json", "w") as file_stream:
        json.dump(statistics, file_stream, indent=4)

    with open(model_output_directory / "predictions.json", "w") as file_stream:
        json.dump(results, file_stream, indent=4)

    model_path_output = model_output_directory / model_name
    model_path_output.write_bytes(model_path.read_bytes())

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
        with open(model_output_directory / (pdf_source_path.stem + ".json"), "w") as file_stream:
            json.dump(settings, file_stream, indent=4)

    for pdf_source_path in pdfs:
        images = [
            p
            for p in Path(pdf_source_path.parent / pdf_source_path.stem).iterdir()
            if p.is_file() and p.suffix == ".png"
        ]
        images.sort()
        responses = []
        for image_path in images:
            model_result = model.execute(str(image_path))
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

    return statistics
