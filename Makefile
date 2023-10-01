install_mode=${1:-poetry}

if [ $install_mode = 'pip' ]; then
  echo "Installing with pip (degraded mode)"
  chmod +x pip-install.sh
  ./pip-install.sh
else
  echo "Installing with poetry (default mode)"
  chmod +x poetry-install.sh
  ./poetry-install.sh
fi
