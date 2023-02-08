from pathlib import Path

from mldesigner import command_component, Input, Output

@command_component(
    display_name="Label And Split Data",
    environment="./environment.conda.yaml",
)
def label_split_data_step(
    labels_input: Input(type="uri_folder"),
    images_input: Input(type="uri_folder"),
    split_images_output: Output(type="uri_folder"),
):
    from label_split_data import label_split_data
    #import mlflow
    labels_files_path = Path(labels_input) / "cats_dogs_others_classification-annotations.json"
    label_split_data(labels_files_path, Path(images_input), Path(split_images_output))
    #mlflow.log_metric("number_files_input", result.number_files_input)
    #mlflow.log_metric("number_images_output", result.number_images_output)
