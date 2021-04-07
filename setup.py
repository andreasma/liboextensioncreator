# -*- coding: utf-8 -*-
"""Installer for the liboextensioncreator package."""

import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="liboextensioncreator",
    version="0.0.1",
    author="Andreas Mantke",
    author_email="maand@gmx.de",
    description="A package to create LibreOffice non-code extensions",
    long_description=long_description,
    url="https://github.com/andreasma/liboextensioncreator",
    project_urls={
        "Bug Tracker": "https://github.com/andreasma/liboextensioncreator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: LGPL 2.1",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)