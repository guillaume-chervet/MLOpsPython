import argparse

from azure.ai.ml.constants import AssetTypes
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

from azure.ai.ml import MLClient, Input, Output, load_component
from azure.ai.ml.dsl import pipeline
from azure.ai.ml.entities import Data
from azure.ai.ml.entities import AmlCompute


import uuid

import json

parser = argparse.ArgumentParser("integration")
parser.add_argument("--subscription_id", type=str)
parser.add_argument("--resource_group_name", type=str)
parser.add_argument("--workspace_name", type=str)
parser.add_argument("--experiment_id", type=str)
parser.add_argument("--integration_dataset_name", type=str)
parser.add_argument("--integration_dataset_version", type=str)
parser.add_argument("--url", type=str)

args = parser.parse_args()
subscription_id = args.subscription_id
resource_group_name = args.resource_group_name
workspace_name = args.workspace_name
experiment_id = args.experiment_id
integration_dataset_name = args.integration_dataset_name
integration_dataset_version = args.integration_dataset_version
url = args.url


URI_FOLDER = "uri_folder"

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
cluster_name = "guillaume-cpu-low"

cluster_basic = AmlCompute(
    name=cluster_name,
    type="amlcompute",
    size="Standard_D4s_v3",
    location="northeurope", #az account list-locations -o table
    min_instances=0,
    max_instances=1,
    idle_time_before_scale_down=60,
)
ml_client.begin_create_or_update(cluster_basic).result()


@pipeline(default_compute=cluster_name)
def azureml_pipeline(integration_input: Input(type=AssetTypes.URI_FOLDER), url_input: Input(type="string")):

    integration_step = load_component(source="mlcli/command.yaml")
    integration = integration_step(
        integration_input=integration_input,
        url_input=url_input
    )

    return {
        "integration_output": integration.outputs.integration_output,
    }


pipeline_job = azureml_pipeline(
    integration_input=Input(
        path="azureml:" + integration_dataset_name + ":" + integration_dataset_version , type=URI_FOLDER
    ),
    url_input=url,
)


azure_blob = "azureml://datastores/workspaceblobstore/paths/"
experience_id = str(uuid.uuid4())

custom_integration_path = azure_blob + "/integration-output/cats-dogs-others/" + experience_id + "/"
pipeline_job.outputs.integration_output = Output(
    type=URI_FOLDER, mode="rw_mount", path=custom_integration_path
)

pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job, experiment_name="cats_dos_others_pipeline"
)

ml_client.jobs.stream(pipeline_job.name)

integration_output_dataset = Data(
    name="cats-dogs-others-integration-output",
    path=custom_integration_path,
    type=URI_FOLDER,
    description="Dataset for credit card defaults",
    tags={"source_type": "web", "source": "UCI ML Repo"},
)
integration_output_dataset = ml_client.data.create_or_update(integration_output_dataset)
print(
    f"Dataset with name {integration_output_dataset.name} was registered to workspace, the dataset version is {integration_output_dataset.version}"
)

output_data = {
    "integration_output_dataset_name": integration_output_dataset.name,
    "integration_output_dataset_version": integration_output_dataset.version
}

print(json.dumps(output_data))