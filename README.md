# pythonwhat

[![Build Status](https://travis-ci.org/datacamp/pythonwhat.svg?branch=master)](https://travis-ci.org/datacamp/pythonwhat)
[![codecov](https://codecov.io/gh/datacamp/pythonwhat/branch/master/graph/badge.svg)](https://codecov.io/gh/datacamp/pythonwhat)
[![PyPI version](https://badge.fury.io/py/pythonwhat.svg)](https://badge.fury.io/py/pythonwhat)
[![Documentation Status](https://readthedocs.org/projects/pythonwhat/badge/?version=stable)](http://pythonwhat.readthedocs.io/en/stable/?badge=stable)

`pythonwhat` enables you to write Submission Correctness Tests (SCTs) for interactive Python exercises on DataCamp.

- If you are new to teaching on DataCamp, check out https://authoring.datacamp.com.
- If you want to learn what SCTs are and how they work, visit [this article](https://authoring.datacamp.com/courses/exercises/technical-details/sct.html) specifically.
- For a complete overview of all functionality inside `pythonwhat` and articles about what to use when, consult https://pythonwhat.readthedocs.io.

## Installation

```bash
# latest stable version from PyPi
pip install pythonwhat

# latest development version from GitHub
pip install git+https://github.com/datacamp/pythonwhat
```

## Demo

Experimenting locally:

```python
from pythonwhat.local import setup_state
s = setup_state(stu_code = "x = 5", sol_code = "x = 4")

s.check_object('x')
# No error: x is defined in both student and solution process

s.check_object('x').has_equal_value()
# Throws error, because value of x is not the same

# Debugging state
s._state               # access state object
dir(s._state)          # list all attributes of the state object
s._state.student_code  # access attribute of state object
```

To include an SCT in a DataCamp course, visit https://authoring.datacamp.com.

## Run tests

Use Python 3.5

```
# install packages used in tests (should be reduced)
pip install -r requirements.txt

# install pythonwhat
cd /path/to/pythonwhat
pip install -e .
pytest
```

To disable deprecation warnings: `$ export PYTHONWARNINGS="ignore"`

For more details, questions and suggestions, contact <b>learn-engineering@datacamp.com</b>.
