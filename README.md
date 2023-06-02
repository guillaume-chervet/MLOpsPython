# MLOpsPython

A real demo of Deep Learning project with preprocessing from development to production using code, ops and Machine Learning best practices. Production is a real time REST API.

Competences
- Code / Debug
- UnitTest, Test Driven Development principles
- Clean Code, Inversion Of Dependence, Functional Programing
- Build & Publish packages
- Git
- Linux Bash
- REST API
- Docker
- Kubernetes

Tools
- Pycharm (https://www.jetbrains.com/pycharm/)
- Python, pip, PipEnv, Conda
- Git & Github & Github Action
- AzureML (https://azure.microsoft.com/fr-fr/free/students?WT.mc_id=DOP-MVP-5003370)
- Docker
- Kubernetes & OpenShift or Azure

## 1. Introduction

The name of our company: MLOps

Today a team of indexers receive 10,000 PDF files a day containing either cats or dogs or something else.
They must manually open each PDF to classify them.

We are going to automate this process. We will use a machine learning model to classify PDF files and expose it as a REST API. It will work in real time.

![project_workflow.png](documentation%2Fproject_workflow.png)

![Supervised_Learning.PNG](documentation%2FSupervised_Learning.PNG)

### Why MLOps ?

Many projects do not ship to production due to many constraints:
 - Expensive 
 - Complex Data Workflow
 - More actors

![Triangle_actors.PNG](documentation%2FTriangle_actors.PNG)

![MLOps_boxes.PNG](documentation%2FMLOps_boxes.PNG)

![Triangle_paint_points.PNG](documentation%2FTriangle_paint_points.PNG)

### What is MLOps?

MLOps is involved in the entire life cycle of an AI project. This is all that will allow your AI project to go into production and then keep your project in production.

No MLOps practices, no production.

![MLOps_is_more_about_human_culture.PNG](documentation%2FMLOps_is_more_about_human_culture.PNG)

### Delivery of a MLOps project

The deliverable of a project is not the AI model, it's how the AI model is generated.

The model must be **reproducible**.

The deliverable is:
- Versioned data
- Versioned code

![MLOps_graal.PNG](documentation%2FMLOps_graal.PNG)

## Project structure
We will use the following project structure. We will use mono-repository git in order to work together. It will help to retrain a model and deploy it in production from one manual action maximum.

![code_organization.PNG](documentation%2Fcode_organization.PNG)

## ML Libraries/Technologies choice

Technologies choices have a huge impact on your development cost.
You cannot use a hundred of libraries and expect to have a good result in a short time.
It will be a nightmare to maintain and to debug.

Enterprises use **Technologies RADAR** to manage and maintain their technologies choice :
https://github.com/axa-group/radar

![ml_libraries_choices.PNG](documentation%2Fml_libraries_choices.PNG)

## 2. Requirements

Download and install:
- Pycharm: https://www.jetbrains.com/pycharm/
- Python 3.11.x : https://www.python.org/downloads/
- Git: https://git-scm.com/downloads
- Docker-desktop: https://www.docker.com/products/docker-desktop/
- Postman: https://www.postman.com/downloads/
- NodeJS 18.x: https://nodejs.org/en/download/

## 3. Getting Started

On windows your have to use "GitBash" only because all commands are linux bash commands.
```sh
git clone https://www.github.com/guillaume-chervet/MLOpsPython

cd MLOpsPython
chmod +x Makefile
./Makefile

# Download the model from here :
# https://github.com/guillaume-chervet/MLOpsPython/releases/download/v0.1.0/mlopspython_model.zip
# Unzip it 
curl -L https://github.com/guillaume-chervet/MLOpsPython/releases/download/v0.1.0/mlopspython_model.zip --output model.zip
unzip model.zip -d ./production/api/core/model
rm model.zip

cd production
docker-compose up
# webapp is now available at : http://localhost:4000
# api is available at : http://localhost:4000/health
```
