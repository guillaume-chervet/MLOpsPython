python -m pip install --upgrade pip
python -m pip install --upgrade setuptools wheel

pip install -e packages/inference

cd packages/inference/
poetry install
poetry build
cd dist
cp *.whl ../../../train/evaluate/packages
cp *.whl ../../../production/api/packages
cd ../../../

pip install -e packages/extraction

cd packages/extraction/
poetry install
poetry build
cd dist
cp *.whl ../../../train/extraction/packages
cp *.whl ../../../production/api/packages
cd ../../../