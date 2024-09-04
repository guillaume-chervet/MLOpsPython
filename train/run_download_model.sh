MODEL_VERSION=$1
AZURE_RESOURCE_GROUP_NAME=$2
AZURE_ML_WORKSPACE_NAME=$3
AZURE_LOCATION=$4
AZURE_SUBSCRIPTION_ID=$5

poetry run python azureml_run_download_model.py \
    --subscription_id "$AZURE_SUBSCRIPTION_ID" \
    --resource_group_name "$AZURE_RESOURCE_GROUP_NAME" \
    --workspace_name "$AZURE_ML_WORKSPACE_NAME" \
    --location "$AZURE_LOCATION" \
    --version "$MODEL_VERSION"

#az ml model download --name cats-dogs-others  \
#    --version "$MODEL_VERSION"  \
#    --resource-group "$AZURE_RESOURCE_GROUP_NAME" \
#    --workspace-name "$AZURE_ML_WORKSPACE_NAME" \
#    --stage "Development"