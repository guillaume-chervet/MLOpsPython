# MLOpsPython

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
- AzureML (https://azure.microsoft.com/fr-fr/free/students/)
- Docker
- Kubernetes & OpenShift

## Introduction

The name of our company: MLOps

Today a team of indexers receive 10,000 PDF files a day containing either cats or dogs or something else.
They must manually open each PDF to classify them.

We are going to automate this process. We will use a machine learning model to classify PDF files and expose it as a REST API. It will work in real time.
![project_workflow.png](documentation%2Fproject_workflow.png)

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

## Setup

Set up Python python 3.11.x on your laptop. You can use venv, conda, etc.

Download PyCharm Pro: https://www.jetbrains.com/pycharm/

First, create git name "MLOpsPython" on your own github account.



```bash
git clone https://github.com/yourusername/MLOpsPython
cd MLOpsPython
# Exclude Pycharm local files from git
echo ".idea" > .gitignore 
```

## Project structure
We will use the following project structure. We will use mono-repository git in order to work together. It will help to retrain a model and deploy it in production from one manual action maximum.

![code_organization.PNG](documentation%2Fcode_organization.PNG)

## Step 1: Extract images from PDF files
[step_1_extraction.md](step_1_extraction.md)

## Step 2: Label images
[step_2_label.md](step_2_label.md)

## Step 3: Label images
[step_3_train.md](step_3_train.md)