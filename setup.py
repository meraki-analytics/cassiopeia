#!/usr/bin/env python

import sys

from setuptools import setup, find_packages


install_requires = [
    "datapipelines>=1.0.7",
    "merakicommons>=1.0.7",
    "Pillow",
    "arrow",
    "requests"
]

# Require python 3.6
if sys.version_info.major != 3 and sys.version_info.minor != 6:
    sys.exit("Cassiopeia requires Python 3.6.")

setup(
    name="cassiopeia",
    version="4.0.9",  # Keep the Cass version at parity with the Riot API major version, use the minor version for breaking changes, and the patch version for everything else
    author="Jason Maldonis; Rob Rua",
    author_email="team@merakianalytics.com",
    url="https://github.com/meraki-analytics/cassiopeia",
    description="Riot Games Developer API Wrapper (3rd Party)",
    keywords=["LoL", "League of Legends", "Riot Games", "API", "REST"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Real Time Strategy",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
    packages=find_packages(),
    zip_safe=True,
    install_requires=install_requires,
    include_package_data=True
)
