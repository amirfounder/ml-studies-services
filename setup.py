from setuptools import setup, find_packages

setup(
    name='daos',
    version='0.1.11',
    packages=find_packages(),
    install_requires=[
        'feedparser~=6.0.8',
        'bs4~=0.0.1',
    ])
