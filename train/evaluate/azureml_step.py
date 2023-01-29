# mldesigner package contains the command_component which can be used to define component from a python function
import logging
from pathlib import Path

from mldesigner import command_component, Input, Output

URI_FOLDER = "uri_folder"


@command_component(
    display_name="Evaluate",
    environment="./environment.conda.yaml",
)
def evaluate_step(
    model_input: Input(type=URI_FOLDER),
    images_input: Input(type=URI_FOLDER),
    model_output: Output(type=URI_FOLDER),
    integration_output: Output(type=URI_FOLDER),
):
    from evaluate import evaluate

    evaluate(logging, Path(model_input), Path(images_input),
             Path(model_output), Path(integration_output))


