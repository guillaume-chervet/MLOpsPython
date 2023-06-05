# MLOpsPython

A real demo of Deep Learning project with preprocessing from development to production using code, ops and Machine Learning best practices. Production is a real time REST API.

![project_workflow.png](documentation%2Fproject_workflow.png)

## Getting Started

Requirements, Download and install:
- Pycharm: https://www.jetbrains.com/pycharm/
- Python 3.11.1 : https://www.python.org/downloads/
- Git: https://git-scm.com/downloads
- Docker-desktop: https://www.docker.com/products/docker-desktop/
- Postman: https://www.postman.com/downloads/
- NodeJS 18.x: https://nodejs.org/en/download/

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

a document sample.pdf is available at :
- "./documentation/postman/sample.pdf"

a postman collection is available at :
- "./documentation/postman/MLOpsPython.postman_collection.json"

## Contribute

- [How to run to contribute](./CONTRIBUTING.md)
- [Please respect our code of conduct](./CODE_OF_CONDUCT.md)
