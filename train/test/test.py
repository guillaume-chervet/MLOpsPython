import json
from pathlib import Path

from mlopspython_inference.inference_pillow import Inference

from integration import prepare_integration_data

model_name = "final_model.keras"


def execute_model_and_generate_integration_test_data(
    logging,
    input_model_directory: Path,
    input_images_directory: Path,
    input_integration_directory: Path,
    model_output_directory: Path,
    integration_output_directory: Path,
):
    logger = logging.getLogger("test")
    model_path = input_model_directory / model_name
    model = Inference(logging, str(model_path))

    statistics = {"ok": 0, "ko": 0, "total": 0}
    results = []
    tests_directory = input_images_directory / "test"
    for path in tests_directory.glob("**/*"):
        if path.is_dir():
            continue
        # keep only files with .png extension
        if path.suffix != ".png":
            continue
        model_result = model.execute(str(path))
        logger.info(f"Prediction for {path}: {model_result}")

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

    prepare_integration_data(input_integration_directory, integration_output_directory, model.execute)

    return statistics

