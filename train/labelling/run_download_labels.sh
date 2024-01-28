resource_group=$1
workspace_name=$2
dataset_name=cats_dogs_others_labels
dataset_version=1

az login
poetry run python run_download_labels.py \
  --project_name "cats_dogs_others_classification" \
  --api_url "https://axaguildev-ecotag.azurewebsites.net/api/server"

echo "Init labels dataset"

RESULT=$(az ml data show --resource-group $resource_group --workspace-name $workspace_name --version $dataset_version --name $dataset_name > /dev/null 2>&1; echo $?)
if [ $RESULT -eq 0 ]; then
  echo "Dataset already exist"
else
  echo "Dataset not found so create it"
  az ml data create -f dataset-labels.yml --resource-group $resource_group --workspace-name $workspace_name

fi

echo "Init label dataset done"
