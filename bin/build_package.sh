
package_directory=$1
train_directory=$2
pipfile_key=$3
pipfile_value=$4
conda_key=$5
conda_value=$6

python -m pip install --upgrade pip
python -m pip install --upgrade setuptools wheel

cwd=$(pwd)

# Generate Hash of files in package and inject it in version.py then build package
PACKAGES_HASH_CLEAN=$(python ./bin/directory_hash.py ./$package_directory)
cd package_directory
echo 'VERSION = "'$PACKAGES_HASH_CLEAN'"' > version.py
echo "build package with version $PACKAGES_HASH_CLEAN"
python setup.py sdist bdist_wheel
cd cwd

# Update package version in env files
python ./bin/replace_in_file.py ./$train_directory/Pipfile $pipfile_key $pipfile_value
python ./bin/replace_in_file.py ./$train_directory/environment.conda.yaml $conda_key $conda_value