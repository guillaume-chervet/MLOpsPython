resource_group=$1
workspace_name=$2
dataset_name=cats_dogs_others
dataset_version=1

echo "Init pdf dataset"

RESULT=$(az ml data show --resource-group $resource_group --workspace-name $workspace_name --version $dataset_version --name $dataset_name > /dev/null 2>&1; echo $?)
if [ $RESULT -eq 0 ]; then
  echo "Dataset already exist"
else
  echo "Dataset not found so create it"
  git clone https://github.com/guillaume-chervet/dataset-cats-dogs-others.git
  rm -rf dataset-cats-dogs-others/.git
  az ml data create -f dataset-cats-dogs-others.yml --resource-group $resource_group --workspace-name $workspace_name

fi

echo "Init pdf dataset done"