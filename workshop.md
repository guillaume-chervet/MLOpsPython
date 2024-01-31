# Workshop MLOps 

Welcome aboard the MLOpsPython team !

You will contribute to the MLOpsPython project.

## 0. Prerequisite

- azure cli https://learn.microsoft.com/fr-fr/cli/azure/install-azure-cli
- github cli https://cli.github.com

- Pycharm (https://www.jetbrains.com/pycharm/)
- Download and install python 3.10.x on your laptop. 
https://www.python.org/downloads/
- Discord (https://discord.com/)
  - Connect to **MTG Lille** (Microsoft Tech Community) to chat with the team : https://discord.com/invite/z5XHgeuNMM 

## 1. Introduction

[Introduction](https://github.com/guillaume-chervet/MLOpsPython/blob/main/documentation/learning.md)

## 2. Getting Started with Postman

You can download some sample .pdf from here : 

https://github.com/guillaume-chervet/dataset-cats-dogs-others

Use Postman to call the API with HTTP POST:
- http://cats-dogs-yolw.northeurope.azurecontainer.io:5000/upload
  - type: form-data
  - key: file 

You can also check health check route with HTTP GET:

http://cats-dogs-yolw.northeurope.azurecontainer.io:5000/health

## 3. Initialize your own project

### 3.1. Create your Azure Account

Important point:
- About azure coupon:
  - DO NOT redeem promo code with an email account that is attached to an EA, the pass will not work.
  - Promo code needs to be redeemed within 90-days of being received.
  - Customer Live ID/Org ID will be limited to one concurrent Azure Pass Sponsorship at a time.
  - Monetary credit can't be used toward third party services, premier support or Azure MarketPlace and cannot be added to existing subscriptions.
  - If you add a payment instrument to the subscription and the subscription is active at the conclusion of the offer it will be converted to Pay-As-You-Go.
  - Subscriptions are activated within minutes of the promo code being redeemed.
- Select **northeurope** region

https://www.microsoftazurepass.com/?WT.mc_id=DOP-MVP-5003370 

Documentation:
https://www.microsoftazurepass.com/Home/HowTo?WT.mc_id=DOP-MVP-5003370 

### 3.2. Fork the GitHub project MLOpsPython

**On Windows**: 
1. Download https://github.com/guillaume-chervet/MLOpsPython/blob/main/bin/init_repository.ps1 PowerShell Script
2. Open a PowerShell Terminal then run 
````ps
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force
./init_repository.ps1
````
3. Go to GitHub Action Tab and activate it !

**On Mac**:

jq and sed are required
1. Download https://github.com/guillaume-chervet/MLOpsPython/blob/main/bin/init_repository.sh Bash Script
2. Open a Bash Terminal then run
````bach
brew install jq
chmod +x ./init_repository.sh
./init_repository.sh
````

**On Linux(Ubuntu)**:

jq and sed are required
1. Download https://github.com/guillaume-chervet/MLOpsPython/blob/main/bin/init_repository.sh Bash Script
2. Open a Bash Terminal then run
````bach
sudo apt update
sudo apt install jq
sudo apt install sed
chmod +x ./init_repository.sh
./init_repository.sh
````


### 3.3. Adapt GitHub Action Parameters

Inside "./.github/workflows/main.yml" file

````bash

env:
  AZURE_RESOURCE_GROUP_NAME: "azure-ml-<your-name>"
  AZURE_ML_WORKSPACE_NAME: "cats-dogs-<your-name>"
  AZURE_WEBAPP_NAME: "cats-dogs-<your-name>"
  DOCKER_IMAGE_NAME: "robertcarry/mlopspython-<your-name>"

````

### 3.4. Run GitHub Action

Commit and push your code

```bash

git add .
git commit -m "Initial commit"
git push origin main

```

This will trigger the GitHub Action.

## 4. Getting Started on your laptop

Follow "Get Started" section to run the project on your laptop :

https://github.com/your-github-login/MLOpsPythonWorkshop

Run the web interface and the API from docker-compose, then you can play with it.


- Pdfs dataset: https://github.com/guillaume-chervet/dataset-cats-dogs-others
- Drift dataset: https://github.com/guillaume-chervet/dataset-cats-dogs-others-drift
- You can test with your own files :)

## 5. First Contribution : Images Labelling

We need you to annotate 200 images of classification of :
- cat
- dog
- other

Authenticate information :
- login: bob
- password: bob

https://axaguildev-ecotag.azurewebsites.net/projects/2329f843-fa3d-45df-bec5-08db0799d5b5

For you culture, Ecotag is an awesome Open Source tool available here :
https://github.com/AxaGuilDEv/ecotag

## 6. Second Contribution : CleanCode & PullRequest

Our team Kanban:

https://github.com/users/guillaume-chervet/projects/1/views/1?layout=board

1. Choose a clean code card on the bord
2. Configure Pycharm to be able to debug existing Tests which are not very clean
3. Create a git branch with a specific unique name

```sh
# Adapt the branch name 
git checkout -b refactor/my_custom_branch_name
```

4. Once task done, push your code and create a PullRequest from GitHub
```sh
git add .
# Please follow a commit convention: https://www.conventionalcommits.org/en/v1.0.0/
git commit -m "refactor(myfonctionnality): commit message"
git push
```

## 7. How to check your API result  

1. Follow "ml-cli" readme and download "ml-cli" version v0.54.2 for your OS https://github.com/AxaFrance/ecotag/blob/master/README-ML-CLI.md
2. Download https://github.com/guillaume-chervet/dataset-cats-dogs-others-mlcli as a zip and unzip content in "demo" folder
     - tasks.json should be in demo directory like "./demo/tasks.json"
4. Adapt tasks.json file to call your API then run ml-cli
5. Once compare file generated, compare the result using ml-cli web UI, you can use the script bellow to navigate inside data

```javascript
try {
    let body = JSON.parse(rawBodyInput);
    const simplerBody = body.map((element) => {
        return {prediction : element.prediction};
    })
    // rawBodyOutput can be updated to format data as you need
    rawBodyOutput = JSON.stringify(simplerBody);
    // writing "isSkipped=true" will remove the item from the results
    isSkipped=false;
} catch(ex) {
    console.log("Left parsing crash");
    console.log(ex.toString());
    rawBodyOutput = rawBodyInput;
}
```

## 8. More AzureML

1. Create a AzureML Compute Instance
2. Open JupyterLab with Python 3.10 and SDK v2
3. Clone the AzureML SDK v2 repository

```sh 
git clone https://github.com/Azure/azureml-examples
cd azureml-examples/sdk/python
```

You are ready to go !
