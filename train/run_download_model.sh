#!/usr/bin/env bash
set -euo pipefail

MODEL_VERSION=$1
AZURE_RESOURCE_GROUP_NAME=$2
AZURE_ML_WORKSPACE_NAME=$3
AZURE_LOCATION=$4
AZURE_SUBSCRIPTION_ID=$5
DOWNLOAD_PATH=$6

# Installer deps du projet "train"
cd "$(dirname "$0")"   # -> train/
uv sync --no-dev

uv run python azureml_run_download_model.py \
  --subscription_id "$AZURE_SUBSCRIPTION_ID" \
  --resource_group_name "$AZURE_RESOURCE_GROUP_NAME" \
  --workspace_name "$AZURE_ML_WORKSPACE_NAME" \
  --location "$AZURE_LOCATION" \
  --version "$MODEL_VERSION" \
  --download_path "$DOWNLOAD_PATH"
