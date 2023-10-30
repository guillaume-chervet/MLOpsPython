python -m ensurepip --upgrade
curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
python get-pip.py
python -m pip install --upgrade pip

python -m pip install setuptools wheel
python -m pip install --upgrade setuptools wheel

cwd=$(pwd)

echo "Install packages Inference"
python -m pip install -e packages/inference

cd packages/inference/
python setup.py sdist bdist_wheel
cd dist
cp *.whl ../../../train/test/packages
cp *.whl ../../../production/api/packages

cd $cwd

echo "Install packages Extraction"
python -m pip install -e packages/extraction

cd packages/extraction/
python setup.py sdist bdist_wheel
cd dist
cp *.whl ../../../train/extraction/packages
cp *.whl ../../../production/api/packages
cd $cwd

