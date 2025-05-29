#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="fit-zfjw-api",
    version="1.0.0",
    author="Lecheeel",
    author_email="",
    description="一个用于FIT教务系统的Python API包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lecheeel/fit-zfjw-api",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    keywords="fit 教务 api 教务系统",
    project_urls={
        "Bug Reports": "https://github.com/Lecheeel/fit-zfjw-api/issues",
        "Source": "https://github.com/Lecheeel/fit-zfjw-api",
    },
    include_package_data=True,
    package_data={
        "fit_zfjw_api": ["utils/ddddocr/*"],
    },
) 