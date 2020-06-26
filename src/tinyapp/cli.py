# -*- coding: utf-8 -*-
"""
TinnyApp.CLI

Command Line Interface Tools.

"""
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from pydoc import locate


def cli_config_file(**kwargs):
    """
    Command Line Interface for ask config argument

    :param kwargs: any additional configuration (i.e. description).
    :return: path to configuration file.
    """
    config = {
        'description': __doc__,
        'args': [{
            'arg': ['--config'],
            'params': {
                'type': 'str',
                'required': True,
                'help': 'path to configuration file (yaml)',
            },
        }],
    }
    config.update(kwargs)
    return parse_args(config).config


def parse_args(config, allow_unknown_args=False):
    """
    Command Line Interface Arguments Parsers

    This is simple wrapper for python's argparse modyle created for
    simple configuration.

    More infor about argparse see: https://docs.python.org/3/library/argparse.html

    Configuration:
        You can provide configuration with dictionary with follow format:

        >>> config = { \\
                'description': 'some optional description for yur app', \\
                'args': [ \\
                    { 'arg': ['-e', '--example'], 'params': { 'type': 'str', 'help': 'example'}}, \\
                ]}

        Please note that params format is argparse fully compatibility.

    Usage:
        >>> args = parse_args(config)

    This example create args parser (argparse) with only one option: -e --example.

    :param config: argparse configuration represented as a dict (see example above).
    :param allow_unknown_args: accept or not unknown (not declired) args.
    :return: if unknown args allowed then return args(Namespace) and unknown_args(list),
             otherwise return only args(Namecpase).
    """
    parser = ArgumentParser(
        description=config.get('description', __doc__),
        formatter_class=RawDescriptionHelpFormatter,
    )
    for i in config['args']:
        a = i.copy()
        if 'type' in a['params']:
            a['params']['type'] = locate(a['params']['type'])
        parser.add_argument(*a['arg'], **a['params'])
    if allow_unknown_args:
        return parser.parse_known_args()
    return parser.parse_args()
