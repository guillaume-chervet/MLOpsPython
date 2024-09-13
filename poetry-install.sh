#!/bin/bash sh
cwd=$(pwd)

function add_dependency {
    package_name=$1
    target_dir=$2

    mkdir -p "$target_dir"
    cp -R "$package_name" "$target_dir"
}

function add_dependencies {
    add_dependency "packages/inference/" "production/api/packages"
    add_dependency "packages/extraction/" "production/api/packages"
}

add_dependencies

python -m pip install -e packages/inference
cd packages/inference/
poetry install
poetry build

python -m pip install -e packages/extraction
cd packages/extraction/
poetry install
poetry build

cd train
poetry install --no-root
cd $cwd

cd train/extraction
poetry install --no-root

cd $cwd
cd train/test
poetry install --no-root

cd $cwd
cd train/train
poetry install --no-root

cd $cwd
cd train/label_split_data
poetry install --no-root

cd $cwd
cd production/api
poetry install --no-root

cd $cwd
cd production/integration
poetry install --no-root