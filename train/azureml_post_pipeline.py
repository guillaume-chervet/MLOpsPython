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
parser.add_argument("--experiment_id", type=str)

args = parser.parse_args()
subscription_id = args.subscription_id
resource_group_name = args.resource_group_name
workspace_name = args.workspace_name
location = args.location
tags = json.loads(args.tags)
experiment_id = args.experiment_id

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

azure_blob = "azureml://datastores/workspaceblobstore/paths/"
path_experiment = azure_blob + "cats-dogs-others/" + experiment_id
custom_extraction_path = (
        path_experiment + "/extraction/"
)

# custom_extraction_hash_path = (
#    azure_blob + "extraction_hash/cats-dogs-others/" + experiment_id + "/"
# )
# pipeline_job.outputs.extraction_hash_output = Output(
#    type=AssetTypes.URI_FOLDER, mode="rw_mount", path=custom_extraction_hash_path
# )

custom_model_path = path_experiment + "/models/"
custom_integration_path = (
        path_experiment + "/integration/"
)

# register_extracted_dataset(
#    ml_client, custom_extraction_hash_path, custom_extraction_path, {}
# )

model_name = "cats-dogs-others"
try:
    model_version = str(len(list(ml_client.models.list(model_name))) + 1)
except:
    model_version = "1"

file_model = Model(
    version=model_version,
    path=custom_model_path,
    type=AssetTypes.CUSTOM_MODEL,
    name=model_name,
    tags={**tags},
    description="Model created from azureML.",
)
saved_model = ml_client.models.create_or_update(file_model)

print(
    f"Model with name {saved_model.name} was registered to workspace, the model version is {saved_model.version}."
)

integration_dataset_name = "cats-dogs-others-integration"
integration_dataset = Data(
    name="cats-dogs-others-integration",
    path=custom_integration_path,
    type=AssetTypes.URI_FOLDER,
    description="Integration dataset for cats and dogs and others",
    tags={**tags},
)
integration_dataset = ml_client.data.create_or_update(integration_dataset)

output_data = {
    "model_version": saved_model.version,
    "model_name": saved_model.name,
    "integration_dataset_name": integration_dataset.name,
    "integration_dataset_version": integration_dataset.version,
    "experiment_id": experiment_id,
}

print(json.dumps(output_data))
