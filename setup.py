#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = "openxenmanager",
    install_requires = ["pygtk", "pydenji"],
    version = "0.1.0", # if possible try keeping sync with spectemplate file
    packages = find_packages(),
    author = "A. G. Rodriguez",
    author_email = "alberto@pesadilla.org",
    description = "openxenmanager",
    license = "GPLv2",
    url = "http://www.openmanager.com", 
)
