resource_group=$1
workspace_name=$2
dataset_name=movie-trailers-labels
dataset_version=1

echo "Init label dataset"

RESULT=$(az ml data show --resource-group $resource_group --workspace-name $workspace_name --version $dataset_version --name $dataset_name > /dev/null 2>&1; echo $?)
if [ $RESULT -eq 0 ]; then
  echo "Dataset already exist"
else
  echo "Dataset not found so create it"
  git clone https://github.com/guillaume-chervet/dataset-cats-dogs-others-labels
  rm -rf dataset-cats-dogs-others-labels/.git
  az ml data create -f movie-trailer-dataset-labels.yml --resource-group $resource_group --workspace-name $workspace_name

fi

echo "Init label dataset done"