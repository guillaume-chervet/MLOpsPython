# Summit AXA

Welcome aboard the MLOpsPython team !

You will contribute to the MLOpsPython project.

First you need to send you GitHub username to Guillaume Chervet send it at :
- to: guillaume.chervet@gmail.com
- title: my github username for MLOPsPython team
- body: youremail@tot.com (email to connect to AzureML)

Then you will receive 2 invitation to join the :
- Github MLOpsPython team.
- AzureML CatsDogsOthers project : https://ml.azure.com/home (you should see project name: Cats-Dogs)

## 1. Introduction

[README.md](README.md)

## 2. Getting Started with Postman

You can download some sample .pdf from here : 

https://github.com/guillaume-chervet/dataset-cats-dogs-others

Use Postman to call the API with HTTP POST:
- https://webapp-cdo.azurewebsites.net/upload
- HTTP POST, type: form-data
- key: file 

You can also check health check route with HTTP GET:

https://webapp-cdo.azurewebsites.net/health

## 3. Getting Started on your laptop

Initialize API python part
```sh
git clone https://www.github.com/guillaume-chervet/MLOpsPython
# on Windows you need to use use gitbash
cd MLOpsPython
chmod +x Makefile
./Makefile

# Download the model from here :
# https://github.com/guillaume-chervet/MLOpsPython/releases/download/v0.0.36/mlopspython_model.zip
# Unzip it 
curl -L https://github.com/guillaume-chervet/MLOpsPython/releases/download/v0.0.32/mlopspython_model.zip --output model.zip
unzip model.zip -d ./production/api/core/model
rm model.zip
```

Run the project with docker-compose
```sh
# From Root folder
cd production
docker-compose up

# Check that everything works here: http://localhost:8000/health
# You should be able to call http://localhost:8000/upload with your postman
# Then, you can open the project with Pycharm Pro
```

Fallback if you do not have docker
```sh
# From Root folder
cd production/api
python index.py 8000
```

Initialize frontend part
```sh
# From Root folder
cd webapp
# you need install nodejs >= 18 : https://nodejs.org/en/download/
npm install
npm start
# Then open browser at http://localhost:4000
# Authenticate information :
# - login: bob
# - password: bob
```

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
