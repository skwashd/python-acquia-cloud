#!/usr/bin/env python

"""Setup ACAPI package."""

from setuptools import setup

setup(
    name='acapi',
    version='0.4.3',
    description='Acquia Cloud API client.',
    author='Dave Hall',
    author_email='me@davehall.com.au',
    url='http://github.com/skwashd/python-acquia-cloud',
    install_requires=['requests==2.11.1', 'requests-cache==0.4.12'],
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=[
        'acapi',
        'acapi.resources',
    ],
)
