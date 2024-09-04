MODEL_VERSION=$1
AZURE_RESOURCE_GROUP_NAME=$2
AZURE_ML_WORKSPACE_NAME=$3

az ml model download --name cats-dogs-others  \
    --version "$MODEL_VERSION"  \
    --resource-group "$AZURE_RESOURCE_GROUP_NAME" \
    --workspace-name "$AZURE_ML_WORKSPACE_NAME"