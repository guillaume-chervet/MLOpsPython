## Fourth step: share python libraries

The data pipeline should be identique between train and production.
It must have :
- Same code
- Same python version
- Idealy same Operating System

### Create your account in pip
https://pypi.org/

### Create a pip token

Create a github action Key PYPI_API_TOKEN and set your newly generated token

### Search and Rename in all files 

- mlopspython_inference => mlopspython_inference_yourname
- mlopspython-inference => mlopspython-inference-yourname

- mlopspython_extraction => mlopspython_extraction_yourname
- mlopspython-extraction => mlopspython-extraction-yourname
