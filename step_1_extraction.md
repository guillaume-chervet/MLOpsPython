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
extracted_images" > .gitignore 
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
    with open(path, "rb") as str:
        with fitz.open(stream=str.read(), filetype="pdf") as d:
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
# run from extraction directory
pipenv run install coverage===7.1.0 --dev
pipenv run coverage run -m unittest tests.extraction_test

```

To have a console feedback
```bash
# run from extraction directory
pipenv run coverage report
echo '
.coverage' >> .gitignore
```

To have a html feedback
```bash
# run from extraction directory
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

### 5. Setup link bewteen AzureML and Github Action

https://learn.microsoft.com/en-us/azure/machine-learning/how-to-github-actions-machine-learning?tabs=userlevel#step-2-authenticate-with-azure

Create a service principal with the az ad sp create-for-rbac command in the Azure CLI. Run this command with Azure Cloud Shell in the Azure portal or by selecting the Try it button.
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

3. Paste the entire JSON output from the Azure CLI command into the secret's value field. Give the secret the name AZUREML_CREDENTIALS.

5. Select Add secret.

### 6. Create your first dataset on AzureML

1. Download Azure Storage Explorer : https://azure.microsoft.com/en-us/products/storage/storage-explorer/

2. Copy local blob to azureML Storage:
```bash
$env:AZCOPY_CRED_TYPE = "Anonymous";
$env:AZCOPY_CONCURRENCY_VALUE = "AUTO";
./azcopy.exe copy "C:\github\MLOpsPython\train\extraction\dataset-cats-dogs-others\" "https://catsdogs5378403836.blob.core.windows.net/raw-data/?sv=2021-10-04&se=2023-03-07T17%3A17%3A58Z&sr=c&sp=rwl&sig=15An06ligcG%2BxfUiAo5rrjUA9W1TMBt6eTEgwojrLoU%3D" --overwrite=prompt --from-to=LocalBlob --blob-type Detect --follow-symlinks --put-md5 --follow-symlinks --disable-auto-decoding=false --recursive --log-level=INFO;
$env:AZCOPY_CRED_TYPE = "";
$env:AZCOPY_CONCURRENCY_VALUE = "";
```