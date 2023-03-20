from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from azure.ai.ml.entities import AmlCompute
from azure.ai.ml import MLClient, Input, Output
from azure.ai.ml.dsl import pipeline

from dumb.components import train_model, score_data, eval_model

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
    subscription_id="3e2cd7cf-84d7-4be2-b701-4ae5779a7fc9",
    resource_group_name="cats-dogs-others-resource",
    workspace_name="cats-dogs-others"
)

# Retrieve an already attached Azure Machine Learning Compute.
cluster_name = "teacher-cpu-low"

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

custom_path = "azureml://datastores/workspaceblobstore/paths/custom_path/${{name}}/"

# define a pipeline with component
@pipeline(default_compute=cluster_name)
def pipeline_with_python_function_components(input_data, test_data, learning_rate):
    """E2E dummy train-score-eval pipeline with components defined via python function components"""

    # Call component obj as function: apply given inputs & parameters to create a node in pipeline
    train_with_sample_data = train_model(
        training_data=input_data, max_epochs=5, learning_rate=learning_rate
    )
    score_with_sample_data = score_data(
        model_input=train_with_sample_data.outputs.model_output, test_data=test_data
    )
    # example how to change path of output on step level,
    # please note if the output is promoted to pipeline level you need to change path in pipeline job level
    score_with_sample_data.outputs.score_output = Output(
        type="uri_folder", mode="rw_mount", path=custom_path
    )
    eval_with_sample_data = eval_model(
        scoring_result=score_with_sample_data.outputs.score_output
    )

    # Return: pipeline outputs
    return {
        "eval_output": eval_with_sample_data.outputs.eval_output,
        "model_output": train_with_sample_data.outputs.model_output,
    }


pipeline_job = pipeline_with_python_function_components(
    input_data=Input(
        path="wasbs://demo@dprepdata.blob.core.windows.net/Titanic.csv", type="uri_file"
    ),
    test_data=Input(
        path="wasbs://demo@dprepdata.blob.core.windows.net/Titanic.csv", type="uri_file"
    ),
    learning_rate=0.1,
)
# example how to change path of output on pipeline level
pipeline_job.outputs.model_output = Output(
    type="uri_folder", mode="rw_mount", path=custom_path
)

pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job, experiment_name="pipeline_samples"
)

# Wait until the job completes
ml_client.jobs.stream(pipeline_job.name)