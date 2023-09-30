import json
from pathlib import Path

from mlopspython_inference.inference_pillow import Inference

model_name = "final_model.keras"

def evaluate(logging, input_model_directory: Path, input_images_directory: Path,
             model_output_directory: Path,
             integration_output_directory: Path):
    model_path = input_model_directory / model_name
    model = Inference(logging, str(model_path))

    statistics = {
                  "ok": 0,
                  "ko": 0,
                  "total": 0
                 }
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
        result = {"filename": path.name,
                  "ok": status,
                  "prediction": prediction,
                  "prediction_truth": prediction_truth,
                  "values": model_result["values"]}
        results.append(result)
    statistics["total"] = statistics["ok"] + statistics["ko"]

    with open(model_output_directory / "statistics.json", 'w') as file_stream:
        json.dump(statistics, file_stream, indent=4)

    with open(model_output_directory / "predictions.json", 'w') as file_stream:
        json.dump(results, file_stream, indent=4)

    model_path_output = model_output_directory / model_name
    model_path_output.write_bytes(model_path.read_bytes())

    mlcli_directory = integration_output_directory / "mlcli"
    mlcli_directory.mkdir(parents=True, exist_ok=True)
    for source_path in tests_directory.glob("**/*"):
        if source_path.is_dir():
            continue
        destination_path = mlcli_directory / source_path.name
        destination_path.write_bytes(source_path.read_bytes())

    ground_truth_directory = integration_output_directory / "ground_truth"
    ground_truth_directory.mkdir(parents=True, exist_ok=True)
    for file in results:
        filename = file["filename"]
        data = {
            "Url": "https://www.groundtruth.fr",
            "FileName": filename,
            "FileDirectory": "",
            "ImageDirectory": "",
            "FrontDefaultStringsMatcher": "",
            "StatusCode": 200,
            "Body": json.dumps(file),
            "Headers": [],
            "TimeMs": 0,
            "TicksAt": 0
        }
        truth_filename = Path(filename).stem + "_" + Path(filename).suffix.lower().replace(".", '') + ".json"
        with open(ground_truth_directory / truth_filename, 'w') as file_stream:
            json.dump(data, file_stream, indent=4)
    return statistics