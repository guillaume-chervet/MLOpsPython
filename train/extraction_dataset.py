import asyncio
from dataclasses import dataclass
from pathlib import Path
import azure.ai.ml._artifacts._artifact_utilities as artifact_utils
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import Data


@dataclass
class RegisterExtractedDataset:
    dataset_version: str
    dataset_name: str


def register_extracted_dataset(ml_client,
                               custom_output_path: str,
                               tags: dict) -> RegisterExtractedDataset | None:
    base_path = Path(__file__).resolve().parent

    artifact_utils.download_artifact_from_aml_uri(
        uri=custom_output_path + "extraction_hash",
        destination=str(base_path),
        datastore_operation=ml_client.datastores,
    )

    # lire le fichier hash.txt qui est dans base_path
    with open(str(base_path / "hash.txt"), "r") as file:
        computed_hash = file.read()
    print(f"computed_hash: {computed_hash}")

    extracted_images_dataset_name = "cats-dogs-others-extracted"
    try:
        list_datasets = ml_client.data.list(extracted_images_dataset_name)
        list_list_dataset = list(list_datasets)
        version_dataset_extraction = len(list_list_dataset) + 1
    except:
        list_list_dataset = []
        version_dataset_extraction = 1
        print("No dataset with name cats-dogs-others-extracted")

    hash_tag_already_exists = False
    len_dataset = len(list_list_dataset)
    if len_dataset > 0:
        dataset = list_list_dataset[len_dataset - 1]
        print(f"dataset.tags: {str(dataset.version)}")
        print(dataset.tags)
        if "hash" in dataset.tags:
            extracted_images_dataset_version = dataset.tags["hash"]
            print(f"extracted_images_dataset_version: {extracted_images_dataset_version}")
            print(f"computed_hash: {computed_hash}")
            if extracted_images_dataset_version == computed_hash:
                hash_tag_already_exists = True

    if not hash_tag_already_exists and "git_head_ref" in tags:  # and tags["git_head_ref"] == "main":
        extracted_images_dataset = Data(
            name=extracted_images_dataset_name,
            path=custom_output_path + "extraction_images",
            type=AssetTypes.URI_FOLDER,
            description="Extracted images for cats and dogs and others",
            version=str(version_dataset_extraction),
            tags={"hash": computed_hash, **tags},
        )
        extracted_images_dataset = ml_client.data.create_or_update(extracted_images_dataset)
        print(
            f"Dataset with name {extracted_images_dataset_name} was registered to workspace, the dataset version is {extracted_images_dataset.version}"
        )
        return RegisterExtractedDataset(dataset_version=extracted_images_dataset.version,
                                        dataset_name=extracted_images_dataset_name)

    return None
