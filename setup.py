#!/usr/bin/env python
# vim: set tabstop=4 shiftwidth=4 textwidth=79 cc=72,79:

from __future__ import print_function
from setuptools import setup, find_packages
setup(
    name = 'python-fire',
    version = '0.1',
    packages = find_packages(),

    scripts = ['python_fire'],

    install_requires = [
        'numpy', 'scipy'
    ],

    author = 'Owain Jones',
    author_email = 'contact@odj.me',
    description = 'Implementation of Fuzzy Intrusion Detection Engine (FIRE)',
    license = 'MIT',
    keywords = 'fuzzy IDS tcpdump nslkdd kddcup fire',
    url = 'https://github.com/erinaceous/python-fire',
)
