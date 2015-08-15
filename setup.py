#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="cassiopeia",
    version="0.0.1",
    author="Rob Rua",
    author_email="robrua@alumni.cmu.edu",
    url="https://github.com/robrua/cassiopeia",
    download_url="https://github.com/robrua/cassiopeia/tarball/0.0.1",
    description="Riot Games Developer API Wrapper (3rd Party)",
    keywords=["LoL", "League of Legends", "Riot Game", "API", "REST"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Real Time Strategy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
    packages=find_packages(),
    zip_safe=True,
    install_requires=[
        "sqlalchemy"
    ]
)
