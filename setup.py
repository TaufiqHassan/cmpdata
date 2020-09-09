"""A setuptools based setup module for acccmip6"""
# -*- coding: utf-8 -*-

from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = [
    'setuptools',
    'pandas',
]

test_requirements = [
    'pytest',
]

setup(
    name='cmdata',
    version='1.0.4',
    description="Package for handling CMIP6 data",
    long_description=readme,
    author="Taufiq Hassan",
    author_email='taufiq.hassanmozumder@email.ucr.edu',
    url='https://github.com/TaufiqHassan/cmdata',
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={
        'console_scripts':[
            'cmdata=cmdata.cli:main',
            ],
        },
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
