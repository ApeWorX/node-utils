#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages  # type: ignore


extras_require = {
    "test": ["pytest>=6.0,<7.0", "pytest-xdist", "pytest-coverage"],
    "lint": [
        "black==20.8b1",
        "flake8==3.8.4",
        "isort>=5.7.0,<6",
        "mypy==0.790",
        "pydocstyle>=5.1.1,<6",
    ],
    "doc": ["Sphinx>=3.4.3,<4", "sphinx_rtd_theme>=0.5.1"],
    "dev": ["pytest-watch>=4.2.0,<5", "wheel", "twine", "ipython"],
}

extras_require["dev"] = (
    extras_require["dev"]
    + extras_require["test"]  # noqa: W504
    + extras_require["lint"]  # noqa: W504
    + extras_require["doc"]  # noqa: W504
)

with open("./README.md") as readme:
    long_description = readme.read()

setup(
    name="node-utils",
    version="0.1.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ApeWorX Ltd.",
    author_email="admin@apeworx.io",
    url="https://github.com/apeworx/node-utils",
    include_package_data=True,
    python_requires=">=3.6, <4",
    install_requires=[],
    extras_require=extras_require,
    py_modules=["node_utils"],
    license="Apache License 2.0",
    zip_safe=False,
    keywords="ethereum",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
