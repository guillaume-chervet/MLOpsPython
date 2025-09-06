# Usage:
#   make download_model_version=0.1.0
#   make download_model_version=0.1.0 UV_ARGS="--no-frozen"
#   bash Makefile 0.1.0
#   bash Makefile 0.1.0 --no-frozen

set -euo pipefail

# --- parse args / env ---
# Si appelé en mode script: 1er argument non optionnel = version
# Sinon: on prend la version via la variable d'env download_model_version (ex: via make)
if [[ "${1-}" != "" && ! "${1}" =~ ^- ]]; then
  download_model_version="${download_model_version:-$1}"
  shift || true
else
  download_model_version="${download_model_version:-none}"
fi

# Le reste des arguments (ou la variable UV_ARGS) sera passé à uv-install.sh
UV_ARGS="${UV_ARGS:-}"
if (( $# > 0 )); then
  # Concatène tous les arguments restants comme args pour uv-install.sh
  UV_ARGS="${UV_ARGS} $*"
fi

if [ "${download_model_version}" != "none" ]; then
  echo ">> Download model v${download_model_version}"
  curl -L "https://github.com/guillaume-chervet/MLOpsPython/releases/download/v${download_model_version}/mlopspython_model.zip" --output model.zip
  mkdir -p ./production/api/core/model
  unzip -o model.zip -d ./production/api/core/model
  rm -f model.zip
  echo ">> Model downloaded."
fi

echo ">> Installing with uv (workspace)"
chmod +x uv-install.sh
# shellcheck disable=SC2086
./uv-install.sh ${UV_ARGS}

echo ">> Done."
