# senior_DE_challanege


# Technologies

- Python >= 3.10
- Pandas
- Docker/Kubernetes for deployment & scale


# Overview

Main packages:

- `data_pipeline.data_loader`: implementation of Data Loader from various data sources and data types
- `tests.test_data_loader`: unit and integration tests for data loader.

# Development
- pip list --format=freeze > requirements.txt
```
cd path/to/project

virtualenv -p python3.10 venv    # Or conda create -n tcb-pool python=3.8
source venv/bin/activate        # Or conda activate tcb-pool
pip install -r requirements.txt

# Set PYTHONPATH for module imports
export PYTHONPATH=path/to/project/folder/
```

# Testings
Run unit tests in `tests/` folder:

```bash
# To run all tests
python -m unittest discover -p *test*.py -v
```

Test coverage: just replace the initial `python` with `coverage run`

```bash
coverage run -m unittest discover -p *test*.py -v

# To show report on console
coverage report -m  # must above 90%

# To show report on Web UI
coverage html
```