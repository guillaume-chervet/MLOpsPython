# ./setup_AzureML.sh <AZURE_SUBSCRIPTION_ID> <AZURE_RESOURCE_GROUP_NAME> <AZURE_ML_WORKSPACE_NAME> <AZURE_LOCATION>
AZURE_SUBSCRIPTION_ID=$1 #az account list
AZURE_RESOURCE_GROUP_NAME=$2
AZURE_ML_WORKSPACE_NAME=$3
AZURE_LOCATION=$4 #az account list-locations -o table


# Initialize Azure ML Workspace
az account set --subscription "$AZURE_SUBSCRIPTION_ID"
az group create --name "$AZURE_RESOURCE_GROUP_NAME" --location "$AZURE_LOCATION"
az extension add -n ml --allow-preview false --yes
# shellcheck disable=SC2086
az ml workspace create -n "$AZURE_ML_WORKSPACE_NAME" -g $AZURE_RESOURCE_GROUP_NAME

# Initialize Azure ML Pdf Dataset
cwd=$(pwd)
cd ./extraction
chmod +x ./init_dataset.sh
./init_dataset.sh "$AZURE_RESOURCE_GROUP_NAME" "$AZURE_ML_WORKSPACE_NAME"
cd $cwd

# Initialize Azure ML Labels Dataset
chmod +x ./run_download_labels.sh
./run_download_labels.sh "$AZURE_RESOURCE_GROUP_NAME" "$AZURE_ML_WORKSPACE_NAME"