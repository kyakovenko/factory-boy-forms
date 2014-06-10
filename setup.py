#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Kirill S. Yakovenko'
__email__ = 'contacts@crystalnix.com'
__copyright__ = 'Copyright 2014, Crystalnix'

import os
import sys

from setuptools import setup

root_dir = os.path.abspath(os.path.dirname(__file__))

PACKAGE = 'factory_forms'

setup(
    name='factory_forms',
    version='0.1',
    description="The extension for Factory Boy",
    author='Kirill S. Yakovenko',
    author_email='kirill.yakovenko@gmail.com',
    url='https://github.com/kyakovenko/factory-boy-forms',
    keywords=['factory_boy_forms', 'factory_forms', 'fixtures'],
    packages=['factory_forms', 'factory_forms.converters'],
    license='MIT',
    setup_requires=[
        'factory_boy>=2.3.1',
        'rstr>=2.1.2',
        'setuptools>=0.8',
    ],
)