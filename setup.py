# -*- coding: utf-8 -*-
import json
import os

import setuptools


def resolve_requirements(enable=True):
    """
    Read requirements from the requirements.txt
    file.
    :return requirements: list of requirements.
    """
    if not enable:
        return []
    with open('requirements.txt', 'r') as req_file:
        return req_file.read().split('\n')


def get_version():
    """
    Read a version from the json package file
    (used by commitezen).
    :return version: return version number as a string.
    """
    with open('package.json') as json_file:
        return json.load(json_file)['version']


setuptools.setup(
    name='zstlib',
    version=get_version(),
    install_requires=resolve_requirements(
        os.getenv('WITH_DEPENDENCIES', None),
    ),
)
