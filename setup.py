#!/usr/bin/env python3

import os
from setuptools import setup

# get key package details from py_pkg/__version__.py
about = {}  # type: ignore
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'boom_base', '__version__.py')) as f:
    exec(f.read(), about)

# load the README file and use it as the long_description for PyPI
with open('README.md', 'r') as f:
    readme = f.read()

# package configuration - for reference see:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#id9
requires = ['flask', 'pymongo', 'requests']

# aliyun-mns
requires.append("pycrypto")
requires.append("aliyun-python-sdk-core-v3>=2.3.5")

setup(
    name=about['__title__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=[
        'boom_base', 'boom_base.model', 'boom_base.flask',
        'boom_base.pubsub', 'boom_base.mns_python_sdk',
        'boom_base.mns_python_sdk.mns'
    ],
    scripts = ["boom_base/mns_python_sdk/bin/mnscmd"],
    include_package_data=True,
    python_requires=">=3.7.*",
    install_requires=requires,
    zip_safe=False,
    keywords='boom base'
)
