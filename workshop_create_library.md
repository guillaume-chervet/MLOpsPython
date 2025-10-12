
# Initalize python package
uv init --package mon_package
cd mon_package

For linux/macos :

source .venv/bin/activate
For windows:

.venv\Scripts\activate

# Runtime dependencies (example)
uv add httpx

# Dev dependencies
uv add --dev pytest pytest-cov ruff black

# Formater / lint (ruff)
uv run ruff check .
uv run ruff format .

# Formater / lint (black)
uv run black . --check
uv run black .



# Run tests & code coverage
uv run pytest -q
uv run pytest -q uv run pytest --cov=mon_package --cov-report=term-missing --cov-report=html

# Build wheel + sdist
uv build

# Publish (PyPI)
uv publish --token "$PYPI_API_TOKEN"

# or TestPyPI
uv publish --repository testpypi --token "$TESTPYPI_API_TOKEN"


# Init Git
git init initial-branch=main
git remote add origin