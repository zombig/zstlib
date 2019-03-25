# -*- coding: utf-8 -*-
import os

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

programming_language = os.getenv('PROG_LANG_VERSION', 2)

if os.getenv('WITH_DEPENDENCIES', False):
    with open('requirements.txt', 'r') as req_file:
        args = {
            'install_requires': req_file.read().split('\n'),
        }
else:
    args = {}

setuptools.setup(
    name='zstlib',
    version='0.1.0',
    author='zombig',
    author_email='zstlib@zombig.name',
    description='Small useful python tool set',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zombig/zstlib',
    packages=setuptools.find_packages(),
    package_data={
        'base_config': ['config.yaml'],
    },
    classifiers=[
        'Programming Language :: Python :: {}'.format(programming_language),
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    **args
)
