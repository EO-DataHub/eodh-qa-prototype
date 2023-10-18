import io
import os
import re
import sys

from setuptools import find_packages
from setuptools import setup

sys.path.append('eodh-qa-prototype')
from _version import __version__


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


setup(
    version=__version__,
    name="eodh-qa-prototype",
    url="https://github.com/EO-DataHub/eodh-qa-prototype",
    license="BSD 2-Clause License",
    author=["Sam Hunt", "Samantha Malone"],
    author_email="sam.hunt@npl.co.uk",
    description="Python package to prototyping components of the EODH QA Check Service",
    long_description=read("README.md"),
    packages=find_packages(exclude=("tests",)),
    install_requires=[],
)
