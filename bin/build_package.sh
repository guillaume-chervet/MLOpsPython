
package_directory=$1
train_directory=$2
package_key=$3
package_value=$4
pip_user=$5
pip_token=$6

python -m pip install --upgrade pip
python -m pip install --upgrade setuptools wheel

cwd=$(pwd)

# Generate Hash of files in package and inject it in version.py then build package
PACKAGES_HASH_CLEAN=$(python ./bin/directory_hash.py ./$package_directory)
cd $package_directory
echo 'VERSION = "'$PACKAGES_HASH_CLEAN'"' > version.py
echo "build package with version $PACKAGES_HASH_CLEAN"
python setup.py sdist bdist_wheel

if [ $pip_token = '__token__' ]; then
  python -m pip install --upgrade twine
  python -m twine upload -u $pip_user -p $pip_token dist/*
else
	echo "Do not publish package because not __token__ user !"
fi


cd $cwd

# Update package version in env files
python ./bin/replace_in_file.py ./$train_directory/Pipfile "{file = \"./packages/$package_key-0.0.0-py3-none-any.whl\"}" "\"===$PACKAGES_HASH_CLEAN\""
python ./bin/replace_in_file.py ./$train_directory/environment.conda.yaml ./packages/$package_key-0.0.0-py3-none-any.whl "$package_value===$PACKAGES_HASH_CLEAN"

if [ -f ./$train_directory/Pipfile.lock ];
then
echo "Pipfile.lock exist so removed"
rm -f ./$train_directory/Pipfile.lock
else
echo "Pipfile.lock is not exist"
fi
sleep 30