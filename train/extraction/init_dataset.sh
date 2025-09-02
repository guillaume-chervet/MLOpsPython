#!/usr/bin/env bash
set -euo pipefail

resource_group=$1
workspace_name=$2
dataset_name="cats_dogs_others"
dataset_version="1"

echo "Init pdf dataset"

if az ml data show \
  --resource-group "$resource_group" \
  --workspace-name "$workspace_name" \
  --name "$dataset_name" \
  --version "$dataset_version" \
  --query id -o tsv >/dev/null 2>&1; then
  echo "Dataset already exists: ${dataset_name}:${dataset_version}"
else
  echo "Dataset not found, creating ${dataset_name}:${dataset_version}"
  git clone https://github.com/guillaume-chervet/dataset-cats-dogs-others.git
  rm -rf dataset-cats-dogs-others/.git
  az ml data create -f dataset-cats-dogs-others.yml --resource-group "$resource_group" --workspace-name "$workspace_name"
fi

echo "Init pdf dataset done"
