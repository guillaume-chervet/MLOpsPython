import setuptools
import version

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="inference",
    version=version.VERSION,
    packages=["inference"],
    package_dir={"": "src"},
    package_data={"inference": ["*"]},
    install_requires=requirements,
    author="Guillaume Chervet",
    include_package_data=True,
    python_requires=">=3.8",
)
