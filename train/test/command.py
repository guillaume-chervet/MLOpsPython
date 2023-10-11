import argparse
from pathlib import Path
from test import execute_model_and_generate_integration_test_data
import mlflow

import logging

parser = argparse.ArgumentParser("test")
parser.add_argument("--model_input", type=str)
parser.add_argument("--images_input", type=str)
parser.add_argument("--integration_input", type=str)
parser.add_argument("--model_output", type=str)
parser.add_argument("--integration_output", type=str)

# Get arguments from parser
args = parser.parse_args()
model_input = args.model_input
images_input = args.images_input
integration_input = args.integration_input
model_output = args.model_output
integration_output = args.integration_output

statistics = execute_model_and_generate_integration_test_data(logging,
                                                              Path(model_input),
                                                              Path(images_input),
                                                              Path(integration_input),
                                                              Path(model_output),
                                                              Path(integration_output))

mlflow.log_metric("ok", statistics["ok"])
mlflow.log_metric("ko", statistics["ko"])
mlflow.log_metric("total", statistics["total"])