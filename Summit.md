# Summit AXA

Welcome abord the MLOpsPython team !

You will contribute to the MLOpsPython project.

First you need to send you GitHub username to Guillaume Chervet send it at :
- to: guillaume.chervet@gmail.com.
- title: my github username for MLOPsPython team
- body: my github username is: [your github username]

Then you will receive an invitation to join the MLOpsPython team.

## 1. Introduction

[README.md](README.md)

## 2. Getting Started with Postman

You can download some sample .pdf from here : https://github.com/guillaume-chervet/dataset-cats-dogs-others

https://webapp-cdo.azurewebsites.net/upload
- HTTP POST, type: form-data
- key: file 

You can also check health check route with HTTP GET:
https://webapp-cdo.azurewebsites.net/health

## 3. Getting Started on your laptop

Initialize python part
```sh

git clone https://www.github.com/guillaume-chervet/MLOpsPython
# on Windows you need to use use gitbash
cd MLOpsPython
./makefile

# Download the model from here :
# https://github.com/guillaume-chervet/MLOpsPython/releases/download/v0.0.32/mlopspython_model.zip
# Unizip it 
curl -L https://github.com/guillaume-chervet/MLOpsPython/releases/download/v0.0.32/mlopspython_model.zip --output model.zip
unzip model.zip -d ./production/api/core

cd production
docker-compose up

# You should be able to call http://localhost:8000/upload with your postman
# Now you can open the project with Pycharm Pro
```

Initialize frontend part
```sh
cd webapp
# you need install nodejs >= 18 : https://nodejs.org/en/download/
npm install
npm start
# then open browser at http://localhost:4000
```

## 4. First Contribution

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

## 5. Second Contribution

Your first PullRequest:
https://github.com/users/guillaume-chervet/projects/1/views/1?layout=board

- Choose a clean code card in the bord
- Configure Pycharm to be able to debug existing Tests which are not very clean
- Create a git branch with a specific unique name 
```sh
# Adapt the branch name 
git checkout -b refactor/my_custom_branch_name
```
- Follow the instructions from teacher about clean code and dependency injection

```sh
# Adapt the branch name 
git checkout -b refactor/my_custom_branch_name
```


- Once task done, push your code and create a PullRequest from GitHub
```sh
git add .
git commit -m "refactor(myfonctionnality): commit message"
git push
```
