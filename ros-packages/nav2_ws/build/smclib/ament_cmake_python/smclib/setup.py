from setuptools import find_packages
from setuptools import setup

setup(
    name='smclib',
    version='4.0.0',
    packages=find_packages(
        include=('smclib', 'smclib.*')),
)
