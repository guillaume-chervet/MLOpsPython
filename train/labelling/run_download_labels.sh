resource_group=$1
workspace_name=$2
dataset_name=cats_dogs_others_labels
dataset_version=1

az login
poetry run python run_downloads_labels.py \
  --jwt_token "eyJhbGciOiJSUzI1NiIsImtpZCI6IkMyNTJGOUNBQjc3Q0MxNTQwNTBFMTg1NTk5MjJCMTJGIiwidHlwIjoiYXQrand0In0.eyJpc3MiOiJodHRwczovL2RlbW8uZHVlbmRlc29mdHdhcmUuY29tIiwibmJmIjoxNzAzMjQ3MDAxLCJpYXQiOjE3MDMyNDcwMDEsImV4cCI6MTcwMzI1MDYwMSwiYXVkIjoiYXBpIiwic2NvcGUiOlsib3BlbmlkIiwicHJvZmlsZSIsImVtYWlsIiwiYXBpIl0sImFtciI6WyJwd2QiXSwiY2xpZW50X2lkIjoiaW50ZXJhY3RpdmUucHVibGljIiwic3ViIjoiMiIsImF1dGhfdGltZSI6MTcwMzI0NTYxNiwiaWRwIjoibG9jYWwiLCJuYW1lIjoiQm9iIFNtaXRoIiwiZW1haWwiOiJCb2JTbWl0aEBlbWFpbC5jb20iLCJzaWQiOiJFNjM2NzJBQTY0MUNCOUZEQTc5NkQ3Mjk0ODI3OUJFNCIsImp0aSI6IjZCMTA3MkVFNTUyMDNFNEI2NzQ0Q0VDQkFBMEE5OTRCIn0.GW3Aykrnb3Vq5xz59X9QuqQdB0i-rExfLvWgUK6D-UyfwP5yM8eh14J-RpTseT_PIzejCGokQ2Bhtehm0A8bAMjtjAYIhJWCgxUNIaUrsIqikYaHxP_ryTD_IlDNchWDfZoWsxUgXcoza8W6-G5RD-zUOiCA9EhIwT7I_HI5Grkf0emng9_0KO5XEofNBU3Y8h1PE27-ZL5WodqQ0Xb6qev407i1G8AUQPhe5H_LtQYNmowCd20DR1qtXztu75OKyT5UayXUhcjTwjD6l-yO-oWoeaCrqOK1pik9QwhyM5urx89--KWJ0vu8N3KePhnBNdae4vmCb9h3FzTxC5f1Mw" \
  --project_name "cats_dogs_others_v1" \
  --api_url "http://localhost:5010/api/server"

echo "Init labels dataset"

RESULT=$(az ml data show --resource-group $resource_group --workspace-name $workspace_name --version $dataset_version --name $dataset_name > /dev/null 2>&1; echo $?)
if [ $RESULT -eq 0 ]; then
  echo "Dataset already exist"
else
  echo "Dataset not found so create it"
  az ml data create -f dataset-labels.yml --resource-group $resource_group --workspace-name $workspace_name

fi

echo "Init label dataset done"
