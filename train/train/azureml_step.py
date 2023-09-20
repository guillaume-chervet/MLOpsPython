from pathlib import Path
from mldesigner import command_component, Input, Output

URI_FOLDER = "uri_folder"


@command_component(
    display_name="Train",
    environment="./environment.conda.yaml",
)
def train_step(
        split_images_input: Input(type=URI_FOLDER),
        model_output: Output(type=URI_FOLDER),
):
    from train import run_test_harness
    import mlflow
    batch_size = 128
    epochs = 2
    params = {
        "batch_size": batch_size,
        "epochs": epochs,
    }
    mlflow.log_params(params)

    mlflow.tensorflow.autolog()
    run_test_harness(Path(split_images_input), Path(model_output), batch_size, epochs)
    #mlflow.log_figure()
    # mlflow.log_metric("number_files_input", result.number_files_input)
    # mlflow.log_metric("number_images_output", result.number_images_output)
