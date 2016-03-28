#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import weakparser

setup(
    name="weakparser",
    version=weakparser.__version__,
    author="Michel Blancard",
    license="MIT",
    description="HTML parser with templates",
    long_description=open('README.md').read(),
    packages=find_packages(),
    url="https://github.com/michelbl/weakparser",
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3'],
    keywords='parser HTML template',
    install_requires=[]
)
