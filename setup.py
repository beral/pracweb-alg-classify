#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup

setup(
    name='PracWeb',
    version='0.1',
    long_description=__doc__,
    packages=['pracweb'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'scikit-learn>=0.13',
        'pybrain',
        'celery>=3'
    ]
)
