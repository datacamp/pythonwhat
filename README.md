# pythonwhat

[![Build Status](https://travis-ci.org/datacamp/pythonwhat.svg?branch=master)](https://travis-ci.org/datacamp/pythonwhat)
[![codecov](https://codecov.io/gh/datacamp/pythonwhat/branch/master/graph/badge.svg)](https://codecov.io/gh/datacamp/pythonwhat)
[![PyPI version](https://badge.fury.io/py/pythonwhat.svg)](https://badge.fury.io/py/pythonwhat)

The `pythonwhat` package provides rich functionality to write Submission Correctness Tests for interactive Python exercises on the DataCamp platform. DataCamp operates with **Python 3**.

For a detailed guide on how to use `pythonwhat`, head over to [the online documentation](http://pythonwhat.readthedocs.io). Before, all documentation was on the [wiki](https://github.com/datacamp/pythonwhat/wiki), but things are steadily being moved to the _readthedocs_ format.

Visit [DataCamp Teach](https://www.datacamp.com/teach) to create your own DataCamp Python course, powered by `pythonwhat`.

## Documentation

* [pythonwhat documentation](http://pythonwhat.readthedocs.io)
* [full tutorial](https://github.com/datacamp/courses-pythonwhat-tutorial)

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
