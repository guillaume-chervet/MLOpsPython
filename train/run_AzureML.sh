#!/usr/bin/env bash
# ./run_AzureML.sh <AZURE_SUBSCRIPTION_ID> <AZURE_RESOURCE_GROUP_NAME> <AZURE_ML_WORKSPACE_NAME> <AZURE_LOCATION> <TAGS_JSON>
set -euo pipefail

AZURE_SUBSCRIPTION_ID=$1
AZURE_RESOURCE_GROUP_NAME=$2
AZURE_ML_WORKSPACE_NAME=$3
AZURE_LOCATION=$4
TAGS=${5:-"{}"}

# S'assurer que les deps du projet "train" sont installées
cd "$(dirname "$0")"   # -> train/
uv sync --no-dev

uv run python azureml_run_pipeline.py \
  --subscription_id "$AZURE_SUBSCRIPTION_ID" \
  --resource_group_name "$AZURE_RESOURCE_GROUP_NAME" \
  --workspace_name "$AZURE_ML_WORKSPACE_NAME" \
  --location "$AZURE_LOCATION" \
  --tags "$TAGS"
