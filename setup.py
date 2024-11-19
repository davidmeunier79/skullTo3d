#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from setuptools import find_packages, setup

test_deps = ['codecov', 'pytest', 'pytest-cov']

flake_deps = ['flake8']

doc_deps = ['sphinx',
            'sphinx-gallery',
            'sphinx_bootstrap_theme',
            'numpydoc',
            'sphinxcontrib-fulltoc',
            'matplotlib']

# requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# version
verstr = "unknown"
try:
    verstrline = open('skullTo3d/_version.py', "rt").read()
except EnvironmentError:
    pass  # Okay, there is no version file.

else:
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
    else:
        raise RuntimeError("unable to find version in yourpackage/_version.py")

print("Will not build conda module")

print("*******************************************************")
print(find_packages())
print("*******************************************************")

setup(
    name="skullTo3d",
    version=verstr,
    packages=find_packages(),
    author="macatools team",
    description="Pipeline for skull extraction for macaque/marmoset",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='BSD 3',
    entry_points={
        'console_scripts': ['segment_petra = workflows.segment_petra:main']},
    extras_require={
        'test': test_deps + flake_deps,
        'doc': flake_deps + test_deps + doc_deps
        },
    install_requires=requirements,
    include_package_data=True)
