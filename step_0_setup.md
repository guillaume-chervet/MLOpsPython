# Setup

## 1. Install python python 3.11.x on your laptop. You can use venv, conda, etc.
https://www.python.org/downloads/

##  2. Download PyCharm Pro 
https://www.jetbrains.com/pycharm/

Pycharm is free for students.
Activate license with your student email address.

##  3. Create a github repository named MLOpsPython on your own github account.
##  4. Clone your own repository

```bash
git clone https://github.com/YOUR-REPOSITORY/MLOpsPython
cd MLOpsPython
```

## 5. Installation of pipenv

https://pipenv.pypa.io/

```bash
pip install --user pipenv
pipenv --python 3.11.1
```

## 6. Configure Pipenv with PyCharm Python Interpreter

https://www.jetbrains.com/help/pycharm/pipenv.html

## 7. Check code quality with Flake8 

https://flake8.pycqa.org/en/latest/

```bash
echo 'print("hellor world hellor world hellor world hellor world hellor world hellor world hellor world hellor world hellor world")
from pathlib import Path
package_dir = Path(__file__).parent.absolute()
print(package_dir)' > demo_flake8.py
```

```bash
pipenv install flake8===6.0.0 --dev
pipenv run flake8
```

You can configure rules using a setup.cfg file
```bash
echo '[flake8]
max-line-length = 122' > setup.cfg
```

Now you can re-run Flake8
```bash
pipenv run flake8
```

## 8. Fix and reformat code with Black

https://black.readthedocs.io

```bash
pipenv install black===23.1.0 --dev
pipenv run black demo_flake8.py
```

You can configure black8 using a pyproject.toml file
```bash
echo '[tool.black]
max-complexity = 10
line-length = 122' > pyproject.toml
```
Now you can re-run black
```bash
pipenv run black
```

https://black.readthedocs.io/en/stable/integrations/editors.html

## 9. Continuous Integration with Github Action

Now you can commit then push your code on github.
```bash
git add . 
commit -m "Initial commit"
git push origin main
```

We create our first github action to check code quality with Flake8 and Black.
```bash
mkdir .github/workflows
cd .github/workflows
echo '
name: Python Cotinuous Integration
on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
permissions:
  contents: read
jobs:
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
    - name: Format with Black
      run: |
        pipenv install --dev
        pipenv run black .
        pipenv run black . --check
    - name: Lint with flake8
      run: |
        pipenv install --dev
        pipenv run flake8 .
' > python-ci.yml
```

Now we can project our main branch on github and check the result of the github action.