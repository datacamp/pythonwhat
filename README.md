# pythonwhat

[![Build Status](https://travis-ci.org/datacamp/pythonwhat.svg?branch=master)](https://travis-ci.org/datacamp/pythonwhat)
[![codecov](https://codecov.io/gh/datacamp/pythonwhat/branch/master/graph/badge.svg)](https://codecov.io/gh/datacamp/pythonwhat)
[![PyPI version](https://badge.fury.io/py/pythonwhat.svg)](https://badge.fury.io/py/pythonwhat)
[![Documentation Status](https://readthedocs.org/projects/pythonwhat/badge/?version=stable)](http://pythonwhat.readthedocs.io/en/stable/?badge=stable)

The `pythonwhat` package helps you to write Submission Correctness Tests (SCTs) for interactive Python exercises on the DataCamp platform.

- If you are new to teaching on DataCamp, check out https://authoring.datacamp.com.
- If you want to learn what SCTs are and how they work, visit https://authoring.datacamp.com/courses/sct.html.
- For a complete overview of all functionality inside `pythonwhat` and articles about what to use when, consult https://pythonwhat.readthedocs.io.

## Documentation

To generate the documentation, install pythonwhat and run..

```
cd docs
make html
```

## Installation

```
pip install git+https://github.com/datacamp/pythonwhat
```

## Run tests

Use Python 3.5

```
# install packages used in tests (should be reduced)
pip install -r requirements.txt

# install pythonbackend (private, for now)
cd path/to/pythonbackend
python3 setup.py install

# install pythonwhat
cd /path/to/pythonwhat
pip install -e .
pytest
```

To disable deprecation warnings: `$ export PYTHONWARNINGS="ignore"`

For more details, questions and suggestions, contact <b>learn-engineering@datacamp.com</b>.
