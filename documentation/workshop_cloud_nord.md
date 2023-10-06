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

https://www.microsoftazurepass.com/Home/HowTo

### 2.2. Create a docker Account

https://www.docker.com/

### 2.3. Fork the GitHub project MLOpsPython

https://github.com/guillaume-chervet/MLOpsPython

### 2.4. Set up Azure Secret > GitHub 

### 2.5. Set up Docker Secret > GitHub 

### 2.6. Adapt GitHub Action Parameters

### 2.7. Run GitHub Action

## 3. Getting Started on your laptop

Follow "Get Started" section:

https://github.com/guillaume-chervet/MLOpsPython

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
https://github.com/AxaGuilDEv/react-oidc

## 5. Second Contribution : CleanCode & PullRequest

Our team Kanban:

https://github.com/users/guillaume-chervet/projects/1/views/1?layout=board

- Choose a clean code card in the bord
- Configure Pycharm to be able to debug existing Tests which are not very clean
- Create a git branch with a specific unique name 
```sh
# Adapt the branch name 
git checkout -b refactor/my_custom_branch_name
```
- Follow instructions from teacher about clean code and dependency injection

- Once task done, push your code and create a PullRequest from GitHub
```sh
git add .
# Please follow a commit convention: https://www.conventionalcommits.org/en/v1.0.0/
git commit -m "refactor(myfonctionnality): commit message"
git push
```
