![banner](https://s3.amazonaws.com/assets.datacamp.com/img/github/content-engineering-repos/pythonwhat_banner_v2.png)

The `pythonwhat` package provides rich functionality to write Submission Correctness Tests for interactive Python exercises on the DataCamp platform. DataCamp operates with **Python 3**.

For a detailed guide on how to use `pythonwhat`, head over to the [wiki](https://github.com/datacamp/pythonwhat/wiki).

Visit [DataCamp Teach](https://www.datacamp.com/teach) to create your own DataCamp Python course, powered by `pythonwhat`.

## Installation

```
pip3 install markdown2
pip3 install git+https://github.com/datacamp/pythonwhat
```

## Run tests

```
# install python backend (private)
sudo pip3 install boto3
cd path/to/pythonbackend
python3 setup.py install

cd /path/to/pythonwhat/tests
ipython3 run_all.py
```




For more details, questions and suggestions, contact <b>content-engineering@datacamp.com</b>.
