from setuptools import setup, find_packages

setup(
    name='services',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'daos @ git+https://github.com/amirfounder/ml-studies-daos',
        'feedparser>=6.0.8',
        'bs4>=0.0.1',
    ])
