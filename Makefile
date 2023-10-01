install_mode=${1:-poetry}

python -m pip install --upgrade pip

if [ $install_mode = 'pip' ]; then
  echo "Installing with pip (degraded mode)"
else
  echo "Installing with poetry (default mode)"
  chmod +x poetry-install.sh
  ./poetry-install.sh
fi
