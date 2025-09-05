#!/usr/bin/env bash
set -euo pipefail

resource_group=$1
workspace_name=$2
dataset_name=cats_dogs_others_labels
dataset_version=1

echo "Init labels dataset"

# Installer deps du projet "train" (où se trouve run_download_labels.py)
cd "$(dirname "$0")"   # -> train/
uv sync --no-dev

if az ml data show --resource-group "$resource_group" --workspace-name "$workspace_name" --version "$dataset_version" --name "$dataset_name" > /dev/null 2>&1; then
  echo "Dataset already exist"
else
  echo "Dataset not found so create it"
  uv run python run_download_labels.py \
    --project_name "cats_dogs_others_classification" \
    --api_url "https://axaguildev-ecotag.azurewebsites.net/api/server"

  az ml data create -f dataset-labels.yml --resource-group "$resource_group" --workspace-name "$workspace_name"
fi

echo "Init label dataset done"
