
echo "Init pdf dataset"

RESULT=$(az ml data show --resource-group azure-ml --workspace-name cats-dogs --version 1 --name cats_dogs_others > /dev/null 2>&1; echo $?)
if [ $RESULT -eq 0 ]; then
  echo "Dataset already exist"
else
  echo "Dataset not found so create it"
  git clone https://github.com/guillaume-chervet/dataset-cats-dogs-others.git
  rm -rf dataset-cats-dogs-others/.git
  az ml data create -f dataset-cats-dogs-others.yml --resource-group azure-ml --workspace-name cats-dogs

fi

RESULT=$(az ml data show --resource-group azure-ml --workspace-name cats-dogs --version 1 --name cats_dogs_others_labels > /dev/null 2>&1; echo $?)
if [ $RESULT -eq 0 ]; then
  echo "Dataset already exist"
else
  echo "Dataset not found so create it"
  git clone https://github.com/guillaume-chervet/dataset-cats-dogs-others-labels.git
  rm -rf dataset-cats-dogs-others-labels/.git
  az ml data create -f dataset-cats-dogs-others-labels.yml --resource-group azure-ml --workspace-name cats-dogs
fi