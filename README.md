# pythonwhat

[![Build Status](https://travis-ci.org/datacamp/pythonwhat.svg?branch=master)](https://travis-ci.org/datacamp/pythonwhat)
[![PyPI version](https://badge.fury.io/py/pythonwhat.svg)](https://badge.fury.io/py/pythonwhat)
[![Documentation Status](https://readthedocs.org/projects/pythonwhat/badge/?version=stable)](http://pythonwhat.readthedocs.io/en/stable/?badge=stable)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fdatacamp%2Fpythonwhat.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fdatacamp%2Fpythonwhat?ref=badge_shield)

Verify Python code submissions and auto-generate meaningful feedback messages. Originally developed for Python exercises on DataCamp for so-called Submission Correctness Tests, but can also be used independently.

- New to teaching on DataCamp? Check out https://instructor-support.datacamp.com
- To learn what SCTs are and how they work, visit [this article](https://instructor-support.datacamp.com/courses/course-development/submission-correctness-tests) specifically.
- For a complete overview of all functionality inside pythonwhat and articles about what to use when, consult https://pythonwhat.readthedocs.io.

## Installation

```bash
# latest stable version from PyPi
pip install pythonwhat

# latest development version from GitHub
pip install git+https://github.com/datacamp/pythonwhat
```

## Demo

To experiment locally, you can use `setup_state()` and write SCTs interactively.
The code throws an error when the underlying checks fail.

```python
# make all checking functions available
from pythonwhat.test_exercise import prep_context
_, ctxt = prep_context()
globals().update(ctxt)

# initialize state with student and solution submission
from pythonwhat.test_exercise import setup_state
setup_state(stu_code = "x = 5", sol_code = "x = 4")

Ex().check_object('x')
# No error: x is defined in both student and solution process

Ex().check_object('x').has_equal_value()
# TestFail: Did you correctly define the variable `x`? Expected `4`, but got `5`.

# Debugging state
Ex()._state               # access state object
dir(Ex()._state)          # list all elements available in the state object
Ex()._state.student_code  # access student_code of state object
```

To learn how to include an SCT in a DataCamp course, visit https://instructor-support.datacamp.com.

## Run tests

```bash
pyenv local 3.9.6
pip3.9 install -r requirements-test.txt
pip3.9 install -e .
pytest
```

## Contributing

Bugs? Questions? Suggestions? [Create an issue](https://github.com/datacamp/pythonwhat/issues/new), or [contact us](mailto:content-engineering@datacamp.com)!


## License

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fdatacamp%2Fpythonwhat.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fdatacamp%2Fpythonwhat?ref=badge_large)
