#!/usr/bin/env python

import re
import ast
from os import path
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

PACKAGE_NAME = 'pythonwhat'
HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md'), encoding='utf-8') as fp:
    README = fp.read()
with open(path.join(HERE, PACKAGE_NAME, '__init__.py'), 'rb') as fp:
    VERSION = str(ast.literal_eval(_version_re.search(
        fp.read().decode('utf-8')).group(1)))

setup(name=PACKAGE_NAME,
      version=VERSION,
      packages=[PACKAGE_NAME, 'pythonwhat.test_funcs'],
      install_requires=["dill", "numpy", "pandas", "markdown2", "jinja2", "asttokens>=1.1.10"],
      long_description=README,
      long_description_content_type='text/markdown',
      license='GNU version 3',
      author='DataCamp',
      author_email='content-engineering@datacamp.com',
      maintainer='Filip Schouwenaars',
      maintainer_email='filip@datacamp.com',
      url='https://github.com/datacamp/pythonwhat')
