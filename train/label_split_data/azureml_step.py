from pathlib import Path

from mldesigner import command_component, Input, Output

@command_component(
    display_name="Label Split Data",
    environment="./environment.conda.yaml",
)
def label_split_data_step(
    labels_input: Input(type="uri_folder"),
    images_input: Input(type="uri_folder"),
    split_images_output: Output(type="uri_folder"),
):
    from label_split_data import label_split_data
    import mlflow

    number_file_by_label = 16
    ratio_train: float = 0.4
    ratio_test: float = 0.3

    params = {
        "number_file_by_label": number_file_by_label,
        "ratio_train": ratio_train,
        "ratio_test": ratio_test
    }

    mlflow.log_params(params)
    labels_files_path = Path(labels_input) / "cats_dogs_others_classification-annotations.json"
    label_split_data_result = label_split_data(labels_files_path,
                                               Path(images_input),
                                               Path(split_images_output),
                                               number_file_by_label,
                                               ratio_train,
                                               ratio_test)
    mlflow.log_metric("number_file_train_by_label", label_split_data_result.number_file_train_by_label)
    mlflow.log_metric("number_file_test_by_label", label_split_data_result.number_file_test_by_label)
    mlflow.log_metric("number_file_evaluate_by_label", label_split_data_result.number_file_evaluate_by_label)
