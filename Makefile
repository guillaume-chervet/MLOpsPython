# Usage:
#   make download_model_version=0.1.0
# ou simplement exécuter ce fichier comme un script bash:
#   bash Makefile 0.1.0

set -euo pipefail

download_model_version="${download_model_version:-${1:-none}}"

if [ "${download_model_version}" != "none" ]; then
  echo ">> Download model v${download_model_version}"
  curl -L "https://github.com/guillaume-chervet/MLOpsPython/releases/download/v${download_model_version}/mlopspython_model.zip" --output model.zip
  mkdir -p ./production/api/core/model
  unzip -o model.zip -d ./production/api/core/model
  rm -f model.zip
  echo ">> Model downloaded."
fi

echo ">> Installing with uv (workspace)"
chmod +x poetry-install.sh
./poetry-install.sh

echo ">> Done."
