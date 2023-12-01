from pathlib import Path

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
import azure.ai.ml._artifacts._artifact_utilities as artifact_utils

def download():
    print('test')
    try:
        credential = DefaultAzureCredential()
        # Check if given credential can get token successfully.
        credential.get_token("https://management.azure.com/.default")
    except Exception as ex:
        print(ex)
        # Fall back to InteractiveBrowserCredential in case DefaultAzureCredential not work
        credential = InteractiveBrowserCredential()
    print('test2')
    ml_client = MLClient(
        credential=credential,
        subscription_id="9d42c9d4-85ab-429d-afb4-4d77f309078c",
        resource_group_name="azure-ml-yola",
        workspace_name="cats-dogs-yola",
    )
    print('test3')
    data_info = ml_client.data.get("cats-dogs-others-integration-output", version="6")
    print('test4')

    BASE_PATH = Path(__file__).resolve().parent
    output_images_directory = BASE_PATH / "data"

    print(data_info.path)
    # Download the dataset
    result = artifact_utils.download_artifact_from_aml_uri(uri = "azureml://subscriptions/9d42c9d4-85ab-429d-afb4-4d77f309078c/resourcegroups/azure-ml-yola/workspaces/cats-dogs-yola/datastores/workspaceblobstore/paths/integration-output/cats-dogs-others/e6c83449-7dff-4106-a159-c4d980109046/", destination = str(output_images_directory), datastore_operation=ml_client.datastores)
    print(result)

    print('test5')
    return result