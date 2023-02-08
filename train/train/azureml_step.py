from pathlib import Path

from mldesigner import command_component, Input, Output

@command_component(
    display_name="Train",
    environment="./environment.conda.yaml",
)
def train_step(
    split_images_input: Input(type="uri_folder"),
    model_output: Output(type="uri_folder"),
):
    from train import run_test_harness
    #import mlflow

    run_test_harness(Path(split_images_input), Path(model_output))
    #mlflow.log_metric("number_files_input", result.number_files_input)
    #mlflow.log_metric("number_images_output", result.number_images_output)
