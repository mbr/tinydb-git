#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='tinydb-git',
    version='0.2.dev1',
    description='A git-based storage backend for tinydb.',
    long_description=read('README.rst'),
    author='Marc Brinkmann',
    author_email='git@marcbrinkmann.de',
    url='https://github.com/mbr/tinydb-git',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=['dulwich', 'tinydb'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
