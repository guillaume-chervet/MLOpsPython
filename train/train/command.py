import argparse
from pathlib import Path

import mlflow
from PIL import Image

from train import run_test_harness

parser = argparse.ArgumentParser("train")
parser.add_argument("--split_images_input", type=str)
parser.add_argument("--model_output", type=str)

# Get arguments from parser
args = parser.parse_args()
split_images_input = args.split_images_input
model_output = args.model_output



batch_size = 64
epochs = 2
params = {
    "batch_size": batch_size,
    "epochs": epochs,
}
mlflow.log_params(params)

mlflow.tensorflow.autolog()
result = run_test_harness(Path(split_images_input), Path(model_output), batch_size, epochs)

mlflow.log_image(Image.open(result.summary_image_path) , "figure.png")
mlflow.log_metric("evaluate_accuracy_percentage", result.evaluate_accuracy_percentage)
