from pathlib import Path

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
import azure.ai.ml._artifacts._artifact_utilities as artifact_utils


def download(subscription_id: str,
             resource_group_name: str,
             workspace_name: str,
             dataset_name: str,
             dataset_version: str,
             ):
    try:
        credential = DefaultAzureCredential()
        # Check if given credential can get token successfully.
        credential.get_token("https://management.azure.com/.default")
    except Exception as ex:
        print(ex)
        # Fall back to InteractiveBrowserCredential in case DefaultAzureCredential not work
        credential = InteractiveBrowserCredential()

    ml_client = MLClient(
        credential=credential,
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        workspace_name=workspace_name,
    )
    data_info = ml_client.data.get(dataset_name, version=dataset_version)
    base_path = Path(__file__).resolve().parent
    output_images_directory = base_path / "dataset"
    if not output_images_directory.exists():
        output_images_directory.mkdir()
    artifact_utils.download_artifact_from_aml_uri(uri=data_info.path,
                                                  destination=str(output_images_directory),
                                                  datastore_operation=ml_client.datastores)
    print("Downloaded dataset name: " + dataset_name + " version: " + dataset_version)
    print(f"output_images_directory: {output_images_directory}")

    return output_images_directory
