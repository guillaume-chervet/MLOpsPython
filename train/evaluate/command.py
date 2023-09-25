import argparse
from pathlib import Path
from evaluate import evaluate
import mlflow

import logging

parser = argparse.ArgumentParser("evaluate")
parser.add_argument("--model_input", type=str)
parser.add_argument("--images_input", type=str)
parser.add_argument("--model_output", type=str)
parser.add_argument("--integration_output", type=str)

# Get arguments from parser
args = parser.parse_args()
model_input = args.model_input
images_input = args.images_input
model_output = args.model_output
integration_output = args.integration_output

statistics = evaluate(logging, Path(model_input), Path(images_input),
         Path(model_output), Path(integration_output))

mlflow.log_metric("ok", statistics["ok"])
mlflow.log_metric("ko", statistics["ko"])
mlflow.log_metric("total", statistics["total"])