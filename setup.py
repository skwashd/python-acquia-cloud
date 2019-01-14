#!/usr/bin/env python

"""Setup ACAPI package."""

import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__name__), 'README.md')) as f:
    long_description = f.read()

setup(
    name='acapi',
    version='0.6.0',
    description='Acquia Cloud API client.',
    long_description=long_description,
    author='Dave Hall',
    author_email='me@davehall.com.au',
    url='http://github.com/skwashd/python-acquia-cloud',
    install_requires=['requests==2.21.0', 'requests-cache==0.4.13'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Internet',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=[
        'acapi',
        'acapi.resources',
    ],
)
