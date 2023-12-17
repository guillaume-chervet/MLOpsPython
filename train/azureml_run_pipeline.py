import argparse

from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

from azure.ai.ml import MLClient, Input, Output, load_component
from azure.ai.ml.dsl import pipeline
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import Data
from azure.ai.ml.entities import AmlCompute

from extraction_dataset import register_extracted_dataset

import uuid

import json

parser = argparse.ArgumentParser("train")
parser.add_argument("--subscription_id", type=str)
parser.add_argument("--resource_group_name", type=str)
parser.add_argument("--workspace_name", type=str)
parser.add_argument("--location", type=str)
parser.add_argument("--tags", type=str, default="{}")

args = parser.parse_args()
subscription_id = args.subscription_id
resource_group_name = args.resource_group_name
workspace_name = args.workspace_name
location = args.location
tags = json.loads(args.tags)

try:
    credential = DefaultAzureCredential()
    # Check if given credential can get token successfully.
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    print(ex)
    # Fall back to InteractiveBrowserCredential in case DefaultAzureCredential not work
    credential = InteractiveBrowserCredential()


# Get a handle to workspace
ml_client = MLClient(
    credential=credential,
    subscription_id=subscription_id,
    resource_group_name=resource_group_name,
    workspace_name=workspace_name,
)

# Retrieve an already attached Azure Machine Learning Compute.
cluster_name = "simple-cpu-low"

cluster_basic = AmlCompute(
    name=cluster_name,
    type="amlcompute",
    size="Standard_D4s_v3",
    location=location,  # az account list-locations -o table
    min_instances=0,
    max_instances=1,
    idle_time_before_scale_down=60,
)
ml_client.begin_create_or_update(cluster_basic).result()


@pipeline(default_compute=cluster_name)
def azureml_pipeline(
    pdfs_input_data: Input(type=AssetTypes.URI_FOLDER),
    labels_input_data: Input(type=AssetTypes.URI_FOLDER),
):
    extraction_step = load_component(source="extraction/command.yaml")
    extraction = extraction_step(pdfs_input=pdfs_input_data)

    label_split_data_step = load_component(source="label_split_data/command.yaml")
    label_split_data = label_split_data_step(
        labels_input=labels_input_data,
        pdfs_input=pdfs_input_data,
        images_input=extraction.outputs.images_output,
    )

    train_step = load_component(source="train/command.yaml")
    train_data = train_step(
        split_images_input=label_split_data.outputs.split_images_output
    )

    test_step = load_component(source="test/command.yaml")
    test_data = test_step(
        model_input=train_data.outputs.model_output,
        integration_input=label_split_data.outputs.split_integration_output,
        images_input=label_split_data.outputs.split_images_output,
    )

    return {
        "extraction_output": extraction.outputs.images_output,
        # "extraction_hash_output": extraction.outputs.hash_output,
        "model_output": test_data.outputs.model_output,
        "integration_output": test_data.outputs.integration_output,
    }


pipeline_job = azureml_pipeline(
    pdfs_input_data=Input(
        path="azureml:cats_dogs_others:1", type=AssetTypes.URI_FOLDER
    ),
    labels_input_data=Input(
        path="azureml:cats_dogs_others_labels:1", type=AssetTypes.URI_FOLDER
    ),
)


azure_blob = "azureml://datastores/workspaceblobstore/paths/"
experiment_id = str(uuid.uuid4())
path_experiment = azure_blob + "cats-dogs-others/" + experiment_id
custom_extraction_path = (
        path_experiment + "/extraction/"
)
pipeline_job.outputs.model_output = Output(
    type=AssetTypes.URI_FOLDER, mode="rw_mount", path=custom_extraction_path
)
# custom_extraction_hash_path = (
#    azure_blob + "extraction_hash/cats-dogs-others/" + experiment_id + "/"
# )
# pipeline_job.outputs.extraction_hash_output = Output(
#    type=AssetTypes.URI_FOLDER, mode="rw_mount", path=custom_extraction_hash_path
# )

custom_model_path = path_experiment + "/models/"
pipeline_job.outputs.model_output = Output(
    type=AssetTypes.URI_FOLDER, mode="rw_mount", path=custom_model_path
)
custom_integration_path = (
        path_experiment + "/integration/"
)
pipeline_job.outputs.integration_output = Output(
    type=AssetTypes.URI_FOLDER, mode="rw_mount", path=custom_integration_path
)

pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job, experiment_name="cats_dos_others_pipeline"
)

ml_client.jobs.stream(pipeline_job.name)

output_data = {
    "experiment_id": experiment_id,
}

print(json.dumps(output_data))
