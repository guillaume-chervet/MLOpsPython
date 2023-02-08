# mldesigner package contains the command_component which can be used to define component from a python function
from mldesigner import command_component, Input, Output



@command_component(
    display_name="Extraction",
    environment="./environment.conda.yaml",
)
def extraction_step(
    pdfs_input: Input(type="uri_folder"),
    images_output: Output(type="uri_folder"),
):
    from extraction import extract_images
    import mlflow

    result = extract_images(pdfs_input, images_output)
    mlflow.log_metric("number_files_input", result.number_files_input)
    mlflow.log_metric("number_images_output", result.number_images_output)
