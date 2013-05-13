#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, Extension

native = Extension('pracweb.native.visual',
                   sources=['native/visual.c'],
                   extra_compile_args=['-std=c99', '-O3'])

setup(
    name='PracWeb',
    version='0.1',
    long_description=__doc__,
    packages=['pracweb'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'PIL',
        'PyYAML',
        'Flask>=0.8',
        'scikit-learn>=0.13',
        'pybrain>=0.3',
        'celery-with-redis>=3'
    ],
    ext_modules=[native],
)
