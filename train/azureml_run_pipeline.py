import argparse

from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

from azure.ai.ml import MLClient, Input, Output, load_component
from azure.ai.ml.dsl import pipeline
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import Data
from azure.ai.ml.entities import AmlCompute

import uuid

import json

parser = argparse.ArgumentParser("train")
parser.add_argument("--subscription_id", type=str)
parser.add_argument("--resource_group_name", type=str)
parser.add_argument("--workspace_name", type=str)

args = parser.parse_args()
subscription_id = args.subscription_id
resource_group_name = args.resource_group_name
workspace_name = args.workspace_name

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
cluster_name = "simple-cpu-low"

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
def azureml_pipeline(pdfs_input_data: Input(type=URI_FOLDER),
                     labels_input_data: Input(type=URI_FOLDER)):
    extraction_step = load_component(source="extraction/command.yaml")
    extraction = extraction_step(
        pdfs_input=pdfs_input_data
    )

    label_split_data_step = load_component(source="label_split_data/command.yaml")
    label_split_data = label_split_data_step(labels_input=labels_input_data,
                                             pdfs_input=pdfs_input_data,
                                             images_input=extraction.outputs.images_output)

    train_step = load_component(source="train/command.yaml")
    train_data = train_step(
        split_images_input=label_split_data.outputs.split_images_output)

    test_step = load_component(source="test/command.yaml")
    test_data = test_step(model_input=train_data.outputs.model_output,
                          integration_input=label_split_data.outputs.integration_output,
                          images_input=label_split_data.outputs.split_images_output)

    return {
        "model_output": test_data.outputs.model_output,
        "integration_output": test_data.outputs.integration_output,
    }


pipeline_job = azureml_pipeline(
    pdfs_input_data=Input(
        path="azureml:cats_dogs_others:1", type=URI_FOLDER
    ),
    labels_input_data=Input(
        path="azureml:cats_dogs_others_labels:1", type=URI_FOLDER
    )
)


azure_blob = "azureml://datastores/workspaceblobstore/paths/"
experiment_id = str(uuid.uuid4())
custom_model_path = azure_blob + "models/cats-dogs-others/" + experiment_id + "/"
pipeline_job.outputs.model_output = Output(
    type=URI_FOLDER, mode="rw_mount", path=custom_model_path
)
custom_integration_path = azure_blob + "/integration/cats-dogs-others/" + experiment_id + "/"
pipeline_job.outputs.integration_output = Output(
    type=URI_FOLDER, mode="rw_mount", path=custom_integration_path
)

pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job, experiment_name="cats_dos_others_pipeline"
)

ml_client.jobs.stream(pipeline_job.name)


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
        description="Model created from azureML.",
    )
saved_model = ml_client.models.create_or_update(file_model)

print(f"Model with name {saved_model.name} was registered to workspace, the model version is {saved_model.version}.")

integration_dataset = Data(
    name="cats-dogs-others-integration",
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
    "model_version": saved_model.version,
    "model_name": saved_model.name,
    "integration_dataset_name": integration_dataset.name,
    "integration_dataset_version": integration_dataset.version,
    "experiment_id": experiment_id,
}

print(json.dumps(output_data))
