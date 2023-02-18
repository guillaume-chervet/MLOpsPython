# mldesigner package contains the command_component which can be used to define component from a python function
import logging
from pathlib import Path

from mldesigner import command_component, Input, Output



@command_component(
    display_name="Evaluate",
    environment="./environment.conda.yaml",
)
def evaluate_step(
    model_input: Input(type="uri_folder"),
    images_input: Input(type="uri_folder"),
    model_output: Output(type="uri_folder"),
    integration_output: Output(type="uri_folder"),
):
    from evaluate import evaluate

    evaluate(loggin=logging, Path(model_input), Path(images_input),
             Path(model_output), Path(integration_output))


