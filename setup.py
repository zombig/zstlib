# -*- coding: utf-8 -*-
import json
import os

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

programming_language = os.getenv('PROG_LANG_VERSION', '2')

if os.getenv('WITH_DEPENDENCIES', None):
    with open('requirements.txt', 'r') as req_file:
        args = {
            'install_requires': req_file.read().split('\n'),
        }
else:
    args = {}


def get_version():
    """
    Read version from package json file,
    that is used for keep current
    :return: str(version)
    """
    with open('package.json') as json_file:
        return json.load(json_file)['version']


setuptools.setup(
    name='zstlib',
    version=get_version(),
    author='zombig',
    author_email='zstlib@zombig.name',
    description='Small useful python tool set',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zombig/zstlib',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: {}'.format(programming_language),
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    **args
)
