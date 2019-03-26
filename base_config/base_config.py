# -*- coding: utf-8 -*-
"""Base Config Module

Handle application configs, loggers and sensu alerts
via yaml configs.

"""
import argparse
import logging
from pydoc import locate

import yaml


class Config(object):
    """Config

    Create application config, set logger and sensu client via provided
    configuration yaml file.

    Example:
        Read config, create logger and send alert
        ```
        from base_config import Config

        cfg = Config()
        cfg.logger.info('config loaded')
        cfg.sensu.ok()
        ```

    """

    def __init__(self, path=None):

        # Pre-defined class vars
        self.sensu = {}
        self.logger = {'name': 'Config Initialization'}
        self.argparse = {
            'description': 'Config Initialization arguments',
            'arguments': {
                'config': {
                    'help': 'path to application config file',
                    'type': 'str',
                    'required': True,
                },
            },
        }

        if not path:
            self.__args_parser()
            path = self.config

        self.__config_parser(path)
        self.__args_parser()
        self.__set_logger()
        self.__set_sensu()
        self.logger.info('Config file loaded from: %s', path)
        self.logger.debug('Current running config: %s', self.__dict__)

    def __set_sensu(self):
        sensu = getattr(self, 'sensu', {})
        if sensu:
            from sensu_client import SensuClient
            sensu.update(sensu.pop('name', self.__class__.__name__))
            self.sensu = SensuClient(**sensu)
        else:
            delattr(self, 'sensu')

    def __config_parser(self, path):
        with open(path) as config_file:
            cfg = yaml.safe_load(config_file)
            assert cfg, 'CONFIG: config file {} is empty!'.format(path)
        for key in cfg.keys():
            setattr(self, key, cfg[key])

    def __args_parser(self):
        args = getattr(self, 'argparse', {})
        if args:
            parser = argparse.ArgumentParser(description=args['description'])
            for arg in args['arguments']:
                arg_prams = args['arguments'][arg].copy()
                arg_prams['type'] = locate(arg_prams['type'])
                arg_prams['default'] = getattr(
                    self, arg, None,
                ) if 'default' not in arg_prams else arg_prams['default']
                parser.add_argument('--{}'.format(arg), **arg_prams)
            delattr(self, 'argparse')
            args = vars(parser.parse_args())
            for arg in args:
                setattr(self, arg, args[arg])

    def __set_logger(self):
        logger_cfg = getattr(self, 'logger')
        self.logger = logging.getLogger(logger_cfg['name'])
        del logger_cfg['name']
        logger_cfg['level'] = logger_cfg.pop('level', 'INFO').upper()
        logger_cfg['format'] = '[%(asctime)s] %(name)s[%(process)d][%(levelname)s]: %(message)s'
        logging.basicConfig(**logger_cfg)
