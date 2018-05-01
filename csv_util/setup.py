#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="csv_util",
    version="0.1.0",
    author="m2fox",
    author_email="dnxbjyj@126.com",
    description="Parse CSV data for human.",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/desion/tidy_page",
    packages=['tidypage'],
    install_requires=[
        "beautifulsoup4",
        lxml_requirement
        ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)
