#!/usr/bin/env python

"""Setup ACAPI package."""

import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__name__), "README.md")) as f:
    long_description = f.read()

setup(
    name="acapi",
    version="0.9.0",
    description="Acquia Cloud API client.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dave Hall",
    author_email="me@davehall.com.au",
    url="http://github.com/skwashd/python-acquia-cloud",
    install_requires=["requests==2.23.0", "requests-cache==0.5.2", "backoff==1.10.0"],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Internet",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["acapi", "acapi.resources"],
)
