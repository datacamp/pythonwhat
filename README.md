![banner](https://s3.amazonaws.com/assets.datacamp.com/img/github/content-engineering-repos/pythonwhat_banner_v2.png)

[![Build Status](https://travis-ci.org/datacamp/pythonwhat.svg?branch=master)](https://travis-ci.org/datacamp/pythonwhat)

The `pythonwhat` package provides rich functionality to write Submission Correctness Tests for interactive Python exercises on the DataCamp platform. DataCamp operates with **Python 3**.

For a detailed guide on how to use `pythonwhat`, head over to [the online documentation](http://pythonwhat.readthedocs.io). Before, all documentation was on the [wiki](https://github.com/datacamp/pythonwhat/wiki), but things are steadily being moved to the _readthedocs_ format.

Visit [DataCamp Teach](https://www.datacamp.com/teach) to create your own DataCamp Python course, powered by `pythonwhat`.

## Documentation

* [pythonwhat documentation](http://pythonwhat.readthedocs.io)
* [full tutorial](https://github.com/datacamp/courses-pythonwhat-tutorial)

## Installation

```
pip3 install markdown2
pip3 install numpy
pip3 install pandas
pip3 install matplotlib
pip3 install git+https://github.com/datacamp/pythonwhat
```

## Run tests

```
# install python backend (private) + required packages
sudo pip3 install boto3
sudo pip3 install bs4
sudo pip3 install h5py
cd path/to/pythonbackend
python3 setup.py install

cd /path/to/pythonwhat
python3 setup.py install
cd tests
python3 run_all.py
```

To disable deprecation warnings: `$ export PYTHONWARNINGS="ignore"`

For more details, questions and suggestions, contact <b>learn-engineering@datacamp.com</b>.
