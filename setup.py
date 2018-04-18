#!/usr/bin/env python

import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('pythonwhat/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
        name='pythonwhat',
        version=version,
        packages=['pythonwhat', 'pythonwhat.test_funcs'],
        install_requires=["dill", "numpy", "pandas", "markdown2", "jinja2"],
        maintainer = 'Michael Chow',
        maintainer_email = 'michael@datacamp.com',
        url = 'https://github.com/datacamp/pythonwhat')
