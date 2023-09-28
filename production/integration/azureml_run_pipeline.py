from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

from azure.ai.ml import MLClient, Input, Output, load_component
from azure.ai.ml.dsl import pipeline
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import Data
from azure.ai.ml.entities import AmlCompute

import uuid

import json
import sys

URI_FOLDER = "uri_folder"

try:
    credential = DefaultAzureCredential()
    # Check if given credential can get token successfully.
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    print(ex)
    # Fall back to InteractiveBrowserCredential in case DefaultAzureCredential not work
    credential = InteractiveBrowserCredential()

arguments = sys.argv
subscription_id = arguments[1]
resource_group_name = arguments[2]
workspace_name = arguments[3]
experiment_id = arguments[4]
integration_dataset_name = arguments[5]
integration_dataset_version = arguments[6]
url = arguments[7]

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
def azureml_pipeline(integration_input_data: Input(type=URI_FOLDER)):

    integration_step = load_component(source="mlcli/command.yaml")
    integration = integration_step(
        integration_input_data=integration_input_data
    )

    return {
        "integration_output": integration.outputs.integration_output,
    }


pipeline_job = azureml_pipeline(
    integration_input_data=Input(
        path="azureml:" + integration_dataset_name + ":" + integration_dataset_version , type=URI_FOLDER
    ),
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

integration_dataset = Data(
    name="cats-dogs-others-integration-output",
    path=custom_integration_path,
    type=URI_FOLDER,
    description="Dataset for credit card defaults",
    tags={"source_type": "web", "source": "UCI ML Repo"},
)
integration_dataset = ml_client.data.create_or_update(integration_dataset)
print(
    f"Dataset with name {integration_dataset.name} was registered to workspace, the dataset version is {integration_dataset.version}"
)

output_data = {
    "integration_output_dataset_name": integration_dataset.name,
    "integration_output_dataset_version": integration_dataset.version
}

print(json.dumps(output_data))