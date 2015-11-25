#!/usr/bin/env python

from setuptools import setup, find_packages


with open('requirements.txt') as fd:
    requirements = fd.readlines()


with open('geotrie/version.py') as fd:
    version = fd.read().split('=')[1].replace("'", '').strip()


with open('README.md') as fd:
    long_description = fd.read()


setup(
    name='geotrie',
    version=version,
    packages=find_packages(exclude=['tests']),
    license='MIT',
    author='Alex Michael',
    author_email='hi@alexmic.net',
    url='https://github.com/alexmic/geotrie-python',
    description='Geospatial search using geohashing, backed by a trie.',
    keywords=['geohash', 'trie', 'spatial', 'search'],
    install_requires=requirements,
    long_description=long_description,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries",
    ]
)
