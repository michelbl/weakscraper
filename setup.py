#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import weakscraper

setup(
    name="weakscraper",
    version=weakscraper.__version__,
    author="Michel Blancard",
    license="MIT",
    description="HTML scraper with templates",
    long_description=open('README.md').read(),
    packages=find_packages(),
    url="https://github.com/michelbl/weakscraper",
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3'],
    keywords='parser scraper HTML template',
    install_requires=[]
)
