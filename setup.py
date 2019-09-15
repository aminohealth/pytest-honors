#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import find_packages, setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-honors",
    version=read("VERSION").strip(),
    author="Amino, Inc",
    author_email="foss@amino.com",
    maintainer="Amino, Inc",
    maintainer_email="foss@amino.com",
    license="MIT",
    url="https://github.com/aminohealth/pytest-honors",
    project_urls={"Documentation": "https://pytest-honors.readthedocs.io/en/latest/"},
    description="Report on tests that honor constraints, and guard against regressions",
    long_description=read("README.rst"),
    packages=find_packages(),
    python_requires=">=3, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=["pytest>=3.5.0"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["honors = pytest_honors"]},
)
