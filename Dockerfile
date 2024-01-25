FROM cimg/python:3.9

COPY . /home/circleci/project

RUN python setup.py sdist bdist_wheel

CMD /bin/bash
