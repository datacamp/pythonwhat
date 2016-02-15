#!/usr/bin/env python

from distutils.core import setup

setup(
	name='pythonwhat',
	version='1.2',
	packages=['pythonwhat'],
	requires=["ast", "re", "markdown2"]
)
