cwd=$(pwd)

function add_dependency {
    package_name=$1
    target_dir=$2

    mkdir -p "$target_dir"
    cp -R "$package_name" "$target_dir"
}

function add_dependencies {
    add_dependency "packages/mlopspython-inference/" "production/api/packages"
    add_dependency "packages/mlopspython-extraction/" "production/api/packages"
}

add_dependencies

POETRY_VERSION=1.8.3
python -m pip install --upgrade pip
python -m pip install --user "poetry==$POETRY_VERSION"

cd packages/mlopspython-inference/
python -m poetry install
python -m poetry build
cd $cwd

cd packages/mlopspython-extraction/
python -m poetry install
python -m poetry build
cd $cwd

cd train
python -m poetry install --no-root
cd $cwd

cd train/extraction
python -m poetry install --no-root

cd $cwd
cd train/test
python -m poetry install --no-root

cd $cwd
cd train/train
python -m poetry install --no-root

cd $cwd
cd train/label_split_data
python -m poetry install --no-root

cd $cwd
cd production/api
python -m poetry install --no-root

cd $cwd
cd production/integration
python -m poetry install --no-root