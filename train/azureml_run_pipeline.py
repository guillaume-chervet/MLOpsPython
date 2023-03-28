from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

from azure.ai.ml import MLClient, Input, Output
from azure.ai.ml.dsl import pipeline
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import Data
from azure.ai.ml.entities import AmlCompute

from extraction.azureml_step import extraction_step
from label_split_data.azureml_step import label_split_data_step
from train.azureml_step import train_step
from evaluate.azureml_step import evaluate_step

import json

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
    subscription_id="9d42c9d4-85ab-429d-afb4-4d77f309078c",
    resource_group_name="azure-ml",
    workspace_name="cats-dogs",
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
def azureml_pipeline(pdfs_input_data, labels_input_data):
    extraction = extraction_step(
        pdfs_input=pdfs_input_data
    )

    label_split_data = label_split_data_step(
        images_input=extraction.outputs.images_output,
        labels_input=labels_input_data)

    train_data = train_step(
        split_images_input=label_split_data.outputs.split_images_output)

    evaluate_data = evaluate_step(model_input=train_data.outputs.model_output,
                                  images_input=label_split_data.outputs.split_images_output)

    return {
        "model_output": evaluate_data.outputs.model_output,
        "integration_output": evaluate_data.outputs.integration_output,
    }


pipeline_job = azureml_pipeline(
    pdfs_input_data=Input(
        path="azureml:cats_dogs_others:1", type=URI_FOLDER
    ),
    labels_input_data=Input(
        path="azureml:cats_dogs_others_labels:2", type=URI_FOLDER
    )
)

custom_model_path = "azureml://datastores/workspaceblobstore/paths/models/cats-dogs-others/"
pipeline_job.outputs.model_output = Output(
    type=URI_FOLDER, mode="rw_mount", path=custom_model_path
)
custom_integration_path = "azureml://datastores/workspaceblobstore/paths/integration/cats-dogs-others/"
pipeline_job.outputs.integration_output = Output(
    type=URI_FOLDER, mode="rw_mount", path=custom_integration_path
)

pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job, experiment_name="cats_dos_others_pipeline"
)

ml_client.jobs.stream(pipeline_job.name)

file_model = Model(
        path=custom_model_path,
        type=AssetTypes.CUSTOM_MODEL,
        name="cats-dogs-others",
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

output_data= {
    "model_version": saved_model.version,
    "model_name": saved_model.name,
    "integration_dataset_name": integration_dataset.name,
    "integration_dataset_version": integration_dataset.version
}

print(json.dumps(output_data))