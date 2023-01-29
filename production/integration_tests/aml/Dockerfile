FROM mcr.microsoft.com/azureml/base:intelmpi2018.3-ubuntu16.04

WORKDIR home

RUN apt-get update
RUN apt-get -y install curl

RUN mkdir ml-cli
RUN cd ml-cli
ENV CURRENT_VERSION=v0.49.6

# Download ml-cli-web
RUN curl -L https://github.com/AxaGuilDEv/ml-cli/releases/download/${CURRENT_VERSION}/ml-cli-linux-x64.zip  --output ml-cli.zip
RUN unzip ml-cli.zip -d ./ml-cli
RUN chmod +x /home/ml-cli/MlCli