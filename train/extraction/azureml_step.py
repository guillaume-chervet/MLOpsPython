# mldesigner package contains the command_component which can be used to define component from a python function
from mldesigner import command_component, Input, Output

from .extraction import extract_images


@command_component(
    display_name="Extraction",
    environment="./env.yaml",
)
def extraction_step(
    pdfs_input: Input(type="uri_folder"),
    images_output: Output(type="uri_folder"),
):

    extract_images(pdfs_input, images_output)
