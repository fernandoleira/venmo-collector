#!/usr/bin/env python3
# coding=utf-8

from setuptools import setup, find_packages
import pip

package_name = 'venmo-collector'

def get_long_description():
    try:
        with open('README.md', 'r') as fn:
            return fn.read()
    except IOError:
        return ''

def get_requirements():
    try:
        with open('requirements.txt', 'r') as fn:
            return fn.read().splitlines()
    except IOError:
        return ''


setup(
    name=package_name,
    version="0.0.1",
    author='Fernando Leira',
    author_email='LeiraFernandoCortel@gmail.com',
    description='Venmo Collector',
    long_description=get_long_description(),
    url="https://github.com/fernandoleira/venmo-collector",
    install_requires=get_requirements(),
    packages=find_packages(),
    include_package_data=True,
    package_dir={package_name: package_name},
    python_requires='>=3.6',
    zip_safe=True
)