# import required libraries
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

from azure.ai.ml import MLClient, Input, Output
from azure.ai.ml.dsl import pipeline
from azure.ai.ml.constants import AssetTypes, InputOutputModes
try:
    credential = DefaultAzureCredential()
    # Check if given credential can get token successfully.
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
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
#cluster_name = "guillaume-cpu-low"
#print(ml_client.compute.get(cluster_name))
cluster_name = "guillaume-cpu-low"
from azure.ai.ml.entities import AmlCompute
cluster_basic = AmlCompute(
    name=cluster_name,
    type="amlcompute",
    size="Standard_D4s_v3",
    location="northeurope", #az account list-locations -o table
    min_instances=0,
    max_instances=1,
    idle_time_before_scale_down=60,
    #tier="low_priority",
)
ml_client.begin_create_or_update(cluster_basic).result()



from extraction.azureml_step import extraction_step

custom_path = "azureml://datastores/workspaceblobstore/paths/custom_path/${{name}}/"

# define a pipeline with component
@pipeline(default_compute=cluster_name)
def azureml_pipeline(input_data):
    extraction = extraction_step(
        pdfs_input=input_data
    )

    return {
        "extraction_output": extraction.outputs.images_output,
    }


pipeline_job = azureml_pipeline(
    input_data=Input(
        path="azureml:cats_dogs_others:1", type="uri_folder"
       # path="azureml:cats_dogs_others:1", type=AssetTypes.URI_FOLDER
    )
)
# example how to change path of output on pipeline level
pipeline_job.outputs.extraction_output = Output(
    type="uri_folder", mode="rw_mount", path=custom_path
   # type=AssetTypes.URI_FOLDER, mode=InputOutputModes.RO_MOUNT, path=custom_path
)

pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job, experiment_name="cats_dos_others_pipeline"
)

# Wait until the job completes
ml_client.jobs.stream(pipeline_job.name)