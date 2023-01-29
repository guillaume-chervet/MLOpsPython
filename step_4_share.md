## Fourth step: share python libraries

The data pipeline should be identique between train and production.
It must have :
- Same code
- Same python version
- Idealy same Operating System

### Remove code from your repository and replace it with the code from this repository

![image](https://user-images.githubusercontent.com/52236059/226585078-0d7cd2dd-b0b5-43bd-bcaa-3b5c6550bbbe.png)

From your project root:
```bash
git add .
git commit -m "replace code from MLOps teacher repository"
git push
```

### Create your account in pip
https://pypi.org/

### Create a pip token

Create a github action Key PYPI_API_TOKEN and set your newly generated token

### Search and Rename in all files 

- mlopspython_inference => mlopspython_inference_yourname
- mlopspython-inference => mlopspython-inference-yourname

- mlopspython_extraction => mlopspython_extraction_yourname
- mlopspython-extraction => mlopspython-extraction-yourname

From your project root:
```bash
git add .
git commit -m "replace code from MLOps teacher repository"
git push
```
