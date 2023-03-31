import json

print(
    f"Dataset with name  was registered to workspace, the dataset version is "
)

output_data = {
    "model_version": 3,
    "model_name": "youhou",
    "integration_dataset_name": "3",
    "integration_dataset_version": "youhou"
}

print(json.dumps(output_data))