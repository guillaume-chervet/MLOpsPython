python -m pip install --upgrade pip
python -m pip install --upgrade setuptools wheel

cwd=$(pwd)

python -m pip install -e packages/inference

cd packages/inference/
poetry install
poetry build
cd dist
cp *.whl ../../../train/evaluate/packages
cp *.whl ../../../production/api/packages
cd $cwd

python -m pip install -e packages/extraction

cd packages/extraction/
poetry install
poetry build
cd dist
cp *.whl ../../../train/extraction/packages
cp *.whl ../../../production/api/packages
cd $cwd


cd train/extraction
poetry export --without-hashes --format=requirements.txt > requirements.txt
sed -i 's#\(.*\)/packages/mlopspython_extraction-0.0.0-py3-none-any.whl\(.*\)#./packages/mlopspython_extraction-0.0.0-py3-none-any.whl\2#' requirements.txt


cd $cwd
cd train/evaluate
poetry export --without-hashes --format=requirements.txt > requirements.txt
sed -i 's#\(.*\)/packages/mlopspython_inference-0.0.0-py3-none-any.whl\(.*\)#./packages/mlopspython_inference-0.0.0-py3-none-any.whl\2#' requirements.txt

cd $cwd
cd train/train
poetry export --without-hashes --format=requirements.txt > requirements.txt
cd $cwd
cd train/label_split_data
poetry export --without-hashes --format=requirements.txt > requirements.txt
cd $cwd