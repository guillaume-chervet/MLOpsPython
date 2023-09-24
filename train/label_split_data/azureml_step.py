from pathlib import Path

from azure.ai.ml.entities import BuildContext
from mldesigner import command_component, Input, Output

URI_FOLDER = "uri_folder"


def get_environment(ml_client):
    from azure.ai.ml.entities import Environment

    environment = Environment(
        build=BuildContext(path="./label_split_data", dockerfile_path="Dockerfile" ),
        name="label_split_data_environment",
        description="Environment created from a Docker image plus Conda environment.",
    )
    ml_client.environments.create_or_update(environment)
    return environment


def get_label_split_data_step(ml_client) -> callable:
    environment = get_environment(ml_client)

    @command_component(
        display_name="Label Split Data",
        environment=environment,
        is_deterministic=True,
    )
    def label_split_data_step(
        labels_input: Input(type=URI_FOLDER),
        images_input: Input(type=URI_FOLDER),
        split_images_output: Output(type=URI_FOLDER),
    ):
        from label_split_data import label_split_data
        import mlflow

        number_file_by_label = 3200
        ratio_train: float = 0.7
        ratio_test: float = 0.2

        params = {"number_file_by_label": number_file_by_label, "ratio_train": ratio_train, "ratio_test": ratio_test}

        mlflow.log_params(params)
        labels_files_path = Path(labels_input) / "cats_dogs_others_classification-annotations.json"
        label_split_data_result = label_split_data(
            labels_files_path,
            Path(images_input),
            Path(split_images_output),
            number_file_by_label,
            ratio_train,
            ratio_test,
        )
        mlflow.log_metric("number_file_train_by_label", label_split_data_result.number_file_train_by_label)
        mlflow.log_metric("number_file_test_by_label", label_split_data_result.number_file_test_by_label)
        mlflow.log_metric("number_file_evaluate_by_label", label_split_data_result.number_file_evaluate_by_label)

    return label_split_data_step
