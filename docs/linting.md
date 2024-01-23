# Installation

## Dependencies

- [Virtualenv](http://www.virtualenv.org/en/latest/)
- [Python 3](http://www.python.org/) (Can be installed using `brew install python3`)


## Lint and pre-commit hooks

To lint with Black and flake8, install pre-commit hooks:
```
. env/bin/activate
pip install -r requirements/generated/requirements-dev.txt
pre-commit install
```

To run them manually:
```
pre-commit run --all-files
```
