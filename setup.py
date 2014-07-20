#!/usr/bin/env python

"""Setup ACAPI package."""

from setuptools import setup

setup(
    name='acapi',
    version='0.1',
    description='Acquia Cloud API client.',
    author='Dave Hall',
    author_email='me@davehall.com.au',
    url='http://github.com/skwashd/python-acquia-cloud',
    install_requires=['httplib2==0.9', 'simplejson==3.5.3', 'six==1.7.3'],
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
        ],
    packages=[
        'acapi',
        'acapi.compat',
        'acapi.resources',
        ],
    )
