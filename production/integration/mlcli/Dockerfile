FROM python:3.10

WORKDIR home

RUN apt-get update
RUN apt-get -y install curl unzip

RUN mkdir ml-cli
WORKDIR /home/ml-cli
ENV CURRENT_VERSION=v0.49.6

# Download ml-cli-web
RUN curl -L https://github.com/AxaGuilDEv/ml-cli/releases/download/${CURRENT_VERSION}/ml-cli-linux-x64.zip --output ml-cli.zip
RUN unzip ml-cli.zip -d ./

RUN chmod +x ./MlCli

CMD ["bash"]
