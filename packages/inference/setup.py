import setuptools

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="mlopspython-inference",
    version="0.0.0",
    packages=["mlopspython_inference"],
    package_dir={"": ""},
    package_data={"mlopspython_inference": ["*"]},
    install_requires=requirements,
    author="Guillaume Chervet",
    include_package_data=True,
    python_requires=">=3.8",
    author_email="guillaume.chervet@gmail.com",
    url='https://github.com/guillaume-chervet/MLOpsPython',
    description="Inference package for MLOpsPython project",
    long_description="Inference package for MLOpsPython project",
    platforms='POSIX',
    classifiers=["Programming Language :: Python :: 3 :: Only",
                 "Programming Language :: Python :: 3.11",
                 ]
)