# Workshop Cloud Nord

Welcome aboard the MLOpsPython team !

You will contribute to the MLOpsPython project.

## 0. Prerequisite

- Pycharm (https://www.jetbrains.com/pycharm/)
- Download and install python 3.10.x on your laptop. 
https://www.python.org/downloads/

## 1. Introduction

[Introduction](https://github.com/guillaume-chervet/MLOpsPython/blob/main/documentation/learning.md)

## 2. Getting Started with Postman

You can download some sample .pdf from here : 

https://github.com/guillaume-chervet/dataset-cats-dogs-others

Use Postman to call the API with HTTP POST:
- http://cats-dogs-yolo.northeurope.azurecontainer.io:5000/upload
  - type: form-data
  - key: file 

You can also check health check route with HTTP GET:

http://cats-dogs-yolo.northeurope.azurecontainer.io:5000/health

## 2. Fork the project MLOpsPython

### 2.1. Create your Azure Account

Important point:
- About azure coupon:
  - DO NOT redeem promo code with an email account that is attached to an EA, the pass will not work.
  - Promo code needs to be redeemed within 90-days of being received.
  - Customer Live ID/Org ID will be limited to one concurrent Azure Pass Sponsorship at a time.
  - Monetary credit can't be used toward third party services, premier support or Azure MarketPlace and cannot be added to existing subscriptions.
  - If you add a payment instrument to the subscription and the subscription is active at the conclusion of the offer it will be converted to Pay-As-You-Go.
  - Subscriptions are activated within minutes of the promo code being redeemed.
- Select **northeurope** region

https://www.microsoftazurepass.com/

Documentation:
https://www.microsoftazurepass.com/Home/HowTo

### 2.3. Fork the GitHub project MLOpsPython

1. Fork https://github.com/guillaume-chervet/MLOpsPython repository
2. Go to GitHub Action Tab and activate it !
3. Clone your new own **MLOpsPython** repository

### 2.4. Set up Azure Secret for GitHub Action

https://learn.microsoft.com/en-us/azure/machine-learning/how-to-github-actions-machine-learning?tabs=userlevel#step-2-authenticate-with-azure?WT.mc_id=DOP-MVP-5003370

Download and install azure-cli from : 

https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli&WT.mc_id=DOP-MVP-5003370

```bash
# Log to azure
az login

# az account show
# >> show your current account
# az account list
# >> list all your account

# set the subscription
az account set -s <subscription-id>

# Create a service principal with the az ad sp create-for-rbac command in the Azure CLI. Run this command with Azure Cloud Shell in the Azure portal or by selecting the Try it button.
```bash
az ad sp create-for-rbac --name "azure-admin" --role contributor \
                            --scopes /subscriptions/<subscription-id> \
                            --sdk-auth
```
In the example above, replace the placeholders with your subscription ID, resource group name, and app name. The output is a JSON object with the role assignment credentials that provide access to your App Service app similar to below. Copy this JSON object for later.

```json
{
    "clientId": "<GUID>",
    "clientSecret": "<GUID>",
    "subscriptionId": "<GUID>",
    "tenantId": "<GUID>",
    (...)
  }
  ```

Create secrets in Github Action

1. In GitHub, go to your repository.
2. Select Security > Secrets and variables > Actions.
3. Select New repository secret.
4. Paste the entire JSON output from the Azure CLI command into the secret's value field. Give the secret the name AZURE_CREDENTIALS.


### 2.5. Set up Docker Secret for GitHub Action 

Create or login to docker hub account: https://www.docker.com/

1. Generate a new access token (Read & Write): https://hub.docker.com/settings/security
2. Create a new secret in your GitHub repository :
   - DOCKER_PASSWORD
   - DOCKER_USERNAME

### 2.6. Adapt GitHub Action Parameters

Inside "./.github/workflows/ci.yml" file

````bash

env:
  AZURE_RESOURCE_GROUP_NAME: "azure-ml-<your-name>"
  AZURE_SUBSCRIPTION_ID: "<subscription-id>"
  AZURE_ML_WORKSPACE_NAME: "cats-dogs-<your-name>"
  AZURE_WEBAPP_NAME: "cats-dogs-<your-name>"
  DOCKER_IMAGE_NAME: "<your-docker-login>/mlopspython"

````

### 2.7. Run GitHub Action

Commit and push your code

```bash

git add .
git commit -m "Initial commit"
git push origin main

```

This will trigger the GitHub Action.

## 3. Getting Started on your laptop

Follow "Get Started" section to run the projet on your laptop :

https://github.com/your-github-login/MLOpsPython

## 4. First Contribution : Images Labelling

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

## 5. Second Contribution : CleanCode & PullRequest

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
