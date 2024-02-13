install_mode=${1:-poetry}
download_model_version=${2:-none}

if [ $download_model_version != 'none' ]; then
	# Download the model from here :
	# https://github.com/guillaume-chervet/MLOpsPython/releases/download/v0.1.0/mlopspython_model.zip
	# Unzip it
	curl -L https://github.com/guillaume-chervet/MLOpsPython/releases/download/v$download_model_version/mlopspython_model.zip --output model.zip
	unzip model.zip -d ./production/api/core/model
	rm model.zip
fi


if [ $install_mode = 'pip' ]; then
  echo "Installing with pip (degraded mode)"
  chmod +x pip-install.sh
  ./pip-install.sh
else
  echo "Installing with poetry (default mode)"
  chmod +x poetry-install.sh
  ./poetry-install.sh
fi
