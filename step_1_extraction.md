## First step: extract image from pdf

In this step, we will setup the project background:
- Code good pratices (clean code unit test)
- Continuous integration via Github Action
- AzureML

### 1. Clean code principle
```bash
mkdir train
cd train
```

Initialize extraction step.
```bash
mkdir extraction
cd extraction
git clone https://github.com/guillaume-chervet/dataset-cats-dogs-others
echo "dataset-cats-dogs-others/
extracted_images/" > .gitignore 
```

Create a virtual environment
```bash
pipenv install
pipenv install "pymupdf===1.21.1"
```

Create extraction.py and __init__.py (so extraction folder is python module)
```bash
echo 'print("init module extraction")' > __init__.py
echo 'from io import BytesIO
from pathlib import Path
import fitz
from fitz import Document, Pixmap

def convert_pixmap_to_rgb(pixmap) -> Pixmap:
    """Convert to rgb in order to write on png"""
    # check if it is already on rgb
    if pixmap.n < 4:
        return pixmap
    else:
        return fitz.Pixmap(fitz.csRGB, pixmap)

pdfs_directory_path = ".\dataset-cats-dogs-others"
images_directory_path = ".\extracted_images"

Path(images_directory_path).mkdir(parents=True, exist_ok=True)
files = [p for p in Path(pdfs_directory_path).iterdir() if p.is_file()]
for path in files:
    with open(path, "rb") as strm:
        with fitz.open(stream=strm.read(), filetype="pdf") as d:
            file_images = []
            nb = len(d) - 1
            for i in range(nb):
                page = d[i]
                imgs = d.get_page_images(i)
                nb_imgs = len(imgs)
                for j, img in enumerate(imgs):
                    xref = img[0]
                    pix = fitz.Pixmap(d, xref)
                    bytes = BytesIO(convert_pixmap_to_rgb(pix).tobytes())
                    fn = path.stem + "_page" + str(i) + "_index" + str(j) + ".png"
                    with open(images_directory_path + "\\" + fn, "wb") as f:
                        f.write(bytes.getbuffer())' > extraction.py
```

The code bellow is very ugly. It not only does not follow the best practices.
It is hard to maintain and to test. We cannot accept that in production.
So we need to clean the code using Pycharm shortcut (https://www.jetbrains.com/help/pycharm/mastering-keyboard-shortcuts.html)

### 2. First Unit Test
https://docs.python.org/3/library/unittest.html

Create a tests directory and create a extraction_test.py file.

```bash
mkdir tests
cd tests
echo 'print("init module extraction.tests")' > __init__.py
```

extraction_test.py
```bash
echo "import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        value = 'foo'.upper()
        expected = 'FOO'
        self.assertEqual(value, expected)

if __name__ == '__main__':
    unittest.main()" > extraction_test.py
```

You can run unit test manually
```bash
# run from extraction directory
pipenv run python -m unittest tests.extraction_test
```

You can now code and debug a real unit test for extraction.py from PyCharm your first unit test.

Coverage
```bash
# run from ./train/extraction directory
pipenv run install coverage===7.1.0 --dev
pipenv run coverage run -m unittest tests.extraction_test

```

To have a console feedback
```bash
# run from ./train/extraction directory
pipenv run coverage report
echo '
.coverage' >> .gitignore
```

To have a html feedback
```bash
# run from ./train/extraction directory
pipenv run coverage html
echo '
htmlcov' >> .gitignore
```

### 3. Update Continuous Integration

Update Github Action pipeline to run unit test.
```yaml
name: Python Continuous Integration
on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
permissions:
  contents: read
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python 3.11
      uses: actions/setup-python@v3
      with:
        python-version: "3.11"
    - name: Install dependencies
      working-directory: train/extraction
      run: |
        python -m pip install --upgrade pip
        pip install --user pipenv
    - name: Format with Black4
      run: |
        pipenv install --dev
        pipenv run black train
        pipenv run black train --check
    - name: Lint with flake8
      run: |
        pipenv install --dev
        pipenv run flake8 .
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python 3.11
      uses: actions/setup-python@v3
      with:
        python-version: "3.11"
    - name: Install dependencies
      working-directory: train/extraction
      run: |
        python -m pip install --upgrade pip
        pip install --user pipenv
    - name: Run unit tests
      working-directory: train/extraction
      run: |
        pipenv install --dev
        pipenv run coverage run -m unittest tests.extraction_test
        pipenv run coverage report
```

### 4. Setup AzureML

Follow instruction with the teacher.

1. Subscribe to Azure with your student email : https://azure.microsoft.com/fr-fr/free/students/?WT.mc_id=DOP-MVP-5003370
2. Search for Azure Machine Learning in the Azure portal
3. Create a new Azure Machine Learning workspace
        
       1 Set as "abonnement": Azure for Students
       2 Set as "groupe de ressource": cats-dogs-others-resource
       3 Set as "nom de l'espace de travail": cats-dogs-others
       4 Validate   
        
![create-azure-ml-workspace.png](documentation%2Fextraction%2Fcreate-azure-ml-workspace.png)

Now your azure ML workspace is created. You can access to it from the Azure portal.

### 5. Create your first AzureML pipeline

1. Create azureml_run_dumb_pipeline.py in train directory like "./train/azureml_run_dumb_pipeline.py"
and replace <subscription-id> <resource-group-name> <workspace-name> and <cluster-name> by your own values.
<cluster-name> can be your firstname-lastname (for example: "guillaume-chervet")

```python 
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

from azure.ai.ml import MLClient, Input, Output
from azure.ai.ml.dsl import pipeline

try:
    credential = DefaultAzureCredential()
    # Check if given credential can get token successfully.
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    # Fall back to InteractiveBrowserCredential in case DefaultAzureCredential not work
    credential = InteractiveBrowserCredential()


# Get a handle to workspace
ml_client = MLClient(
    credential=credential,
    subscription_id="<subscription-id>",
    resource_group_name="<resource-group-name>",
    workspace_name="<workspace-name>",
)

# Retrieve an already attached Azure Machine Learning Compute.
cluster_name = "<cluster-name>"
from azure.ai.ml.entities import AmlCompute
cluster_basic = AmlCompute(
    name=cluster_name,
    type="amlcompute",
    size="Standard_D4s_v3",
    location="northeurope", #az account list-locations -o table
    min_instances=0,
    max_instances=1,
    idle_time_before_scale_down=60,
)
ml_client.begin_create_or_update(cluster_basic).result()


from dumb.components import train_model, score_data, eval_model

custom_path = "azureml://datastores/workspaceblobstore/paths/custom_path/${{name}}/"

# define a pipeline with component
@pipeline(default_compute=cluster_name)
def pipeline_with_python_function_components(input_data, test_data, learning_rate):
    """E2E dummy train-score-eval pipeline with components defined via python function components"""

    # Call component obj as function: apply given inputs & parameters to create a node in pipeline
    train_with_sample_data = train_model(
        training_data=input_data, max_epochs=5, learning_rate=learning_rate
    )
    score_with_sample_data = score_data(
        model_input=train_with_sample_data.outputs.model_output, test_data=test_data
    )
    # example how to change path of output on step level,
    # please note if the output is promoted to pipeline level you need to change path in pipeline job level
    score_with_sample_data.outputs.score_output = Output(
        type="uri_folder", mode="rw_mount", path=custom_path
    )
    eval_with_sample_data = eval_model(
        scoring_result=score_with_sample_data.outputs.score_output
    )

    # Return: pipeline outputs
    return {
        "eval_output": eval_with_sample_data.outputs.eval_output,
        "model_output": train_with_sample_data.outputs.model_output,
    }


pipeline_job = pipeline_with_python_function_components(
    input_data=Input(
        path="wasbs://demo@dprepdata.blob.core.windows.net/Titanic.csv", type="uri_file"
    ),
    test_data=Input(
        path="wasbs://demo@dprepdata.blob.core.windows.net/Titanic.csv", type="uri_file"
    ),
    learning_rate=0.1,
)
# example how to change path of output on pipeline level
pipeline_job.outputs.model_output = Output(
    type="uri_folder", mode="rw_mount", path=custom_path
)

pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job, experiment_name="pipeline_samples"
)

# Wait until the job completes
ml_client.jobs.stream(pipeline_job.name)
```

2. Create a dumb directory in train directory
```bash
# run from ./train directory
mkdir dumb
```

3. Create a components.py file in dumb directory
```python
# run from ./train/dumb directory
from pathlib import Path
from random import randint
from uuid import uuid4

# mldesigner package contains the command_component which can be used to define component from a python function
from mldesigner import command_component, Input, Output


@command_component()
def train_model(
    training_data: Input(type="uri_file"),
    max_epochs: int,
    model_output: Output(type="uri_folder"),
    learning_rate=0.02,
):
    """A dummy train component.

    Args:
        training_data: a file contains training data
        max_epochs: max epochs
        learning_rate: learning rate
        model_output: target folder to save model output
    """

    lines = [
        f"Training data path: {training_data}",
        f"Max epochs: {max_epochs}",
        f"Learning rate: {learning_rate}",
        f"Model output path: {model_output}",
    ]

    for line in lines:
        print(line)

    # Do the train and save the trained model as a file into the output folder.
    # Here only output a dummy data for demo.
    model = str(uuid4())
    (Path(model_output) / "model").write_text(model)


@command_component(
    display_name="Score",
    # init customer environment with conda YAML
    # the YAML file shall be put under your code folder.
    environment="./environment.conda.yaml",
    # specify your code folder, default code folder is current file's parent
    # code='.'
)
def score_data(
    model_input: Input(type="uri_folder"),
    test_data: Input(type="uri_file"),
    score_output: Output(type="uri_folder"),
):
    """A dummy score component."""

    lines = [
        f"Model path: {model_input}",
        f"Test data path: {test_data}",
        f"Scoring output path: {score_output}",
    ]

    for line in lines:
        print(line)

    # Load the model from input port
    # Here only print the model as text since it is a dummy one
    model = (Path(model_input) / "model").read_text()
    print("Model:", model)

    # Do scoring with the input model
    # Here only print text to output file as demo
    (Path(score_output) / "score").write_text("scored with {}".format(model))


@command_component(display_name="Evaluate", environment="./environment.conda.yaml")
def eval_model(
    scoring_result: Input(type="uri_folder"), eval_output: Output(type="uri_folder")
):
    """A dummy evaluate component."""

    lines = [
        f"Scoring result path: {scoring_result}",
        f"Evaluation output path: {eval_output}",
    ]

    for line in lines:
        print(line)

    # Evaluate the incoming scoring result and output evaluation result.
    # Here only output a dummy file for demo.
    (Path(eval_output) / "eval_result").write_text("eval_result")

```

4. Create a environment.conda.yaml file in dumb directory
```yaml
# run from ./train/dumb directory
image: mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04
name: mldesigner_environment
conda_file:
  name: default_environment
  channels:
    - defaults
  dependencies:
    - python=3.8.12
    - pip=21.2.2
    - pip:
      - mldesigner==0.1.0b4
      
```

5. Create empty Pipfile in train directory like "./train/Pipfile" then run
```bash
# run from ./train directory
pipenv install azure-ai-ml==1.4.0 mldesigner==0.1.0b11
```

6. Now you can run your first AzureML pipeline
```bash
# run from ./train directory
pipenv run python azureml_run_dumb_pipeline.py
```

### 5. Setup link bewteen AzureML and Github Action

https://learn.microsoft.com/en-us/azure/machine-learning/how-to-github-actions-machine-learning?tabs=userlevel#step-2-authenticate-with-azure?WT.mc_id=DOP-MVP-5003370

Download and install azure-cli from : 

https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli&WT.mc_id=DOP-MVP-5003370

```bash
# Log to azure
az login
# set the subscription
az account set -s <subscription-id>

# Create a service principal with the az ad sp create-for-rbac command in the Azure CLI. Run this command with Azure Cloud Shell in the Azure portal or by selecting the Try it button.
```bash
az ad sp create-for-rbac --name "myML" --role contributor \
                            --scopes /subscriptions/<subscription-id>/resourceGroups/<group-name> \
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

4. Paste the entire JSON output from the Azure CLI command into the secret's value field. Give the secret the name AZUREML_CREDENTIALS.

5. Update your github action workflow file to use the secret and run AzureML pipeline. You must run this task only if unit test are passing.

```yaml
    - name: azure login
      uses: azure/login@v1
      with:
        creds: ${{secrets.AZUREML_CREDENTIALS}}
    - name: run train/azure/run_pipeline.py.py
      run: |
          pipenv install
          pipenv run python azureml_run_dumb_pipeline.py
      working-directory: train
```

### 6. Create your first dataset on AzureML
1. Download Azure Storage Explorer : 

https://azure.microsoft.com/en-us/products/storage/storage-explorer?WT.mc_id=DOP-MVP-5003370

Follow teacher instruction and connect with your Azure account.

2. Install AzureML extension to az cli : 

https://learn.microsoft.com/en-us/azure/machine-learning/how-to-configure-cli?WT.mc_id=DOP-MVP-5003370

```bash
az extension add -n ml
```

3. Create a "Folder" asset: 

https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-data-assets?WT.mc_id=DOP-MVP-5003370

```bash
# run from ./train/extraction directory
echo '
$schema: https://azuremlschemas.azureedge.net/latest/data.schema.json

# Supported paths include:
# local: ./<path>
# blob:  https://<account_name>.blob.core.windows.net/<container_name>/<path>
# ADLS gen2: abfss://<file_system>@<account_name>.dfs.core.windows.net/<path>/
# Datastore: azureml://datastores/<data_store_name>/paths/<path>
type: uri_folder
name: cats_dogs_others
description: Cats Dogs and Others
path: ./dataset-cats-dogs-others
' > dataset-cats-dogs-others.yml
``` 

Now you can create and upload your first dataset:
```bash
# run from ./train/extraction directory
az ml data create -f dataset-cats-dogs-others.yml
``` 

