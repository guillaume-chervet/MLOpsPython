import setuptools
import version

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="mlopspython-extraction",
    version=version.VERSION,
    packages=["mlopspython_extraction"],
    package_dir={"": ""},
    package_data={"mlopspython_extraction": ["*"]},
    install_requires=requirements,
    author="Guillaume Chervet",
    include_package_data=True,
    python_requires=">=3.8",
    author_email="guillaume.chervet@gmail.com",
    url='https://github.com/guillaume-chervet/MLOpsPython',
    description="Extraction package for MLOpsPython project",
    long_description="Extraction package for MLOpsPython project",
    platforms='POSIX',
    classifiers=["Programming Language :: Python :: 3 :: Only",
                 "Programming Language :: Python :: 3.11",
                 ]
)