import os

import yaml


class Config(object):

    def __init__(self, path=None):
        path = path if path else os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "{}.yaml".format(self.__class__.__name__.lower()),
        )
        self.__config_parser(path)
        self.__args_parser()
        self.__set_logger()
        if getattr(self, 'sensu', None):
            from sensu_client import SensuClient
            name = self.sensu.pop('name', self.__class__.__name__)
            self.sensu = SensuClient(
                name=name, **self.sensu
            )
        self.logger.info('Program called by class {}'.format(
            self.__class__.__name__,
        ))
        self.logger.info('Config file loaded from: {}'.format(path))
        self.logger.debug('Current running config: {}'.format(self.__dict__))

    def __config_parser(self, path):
        with open(path) as config_file:
            cfg = yaml.safe_load(config_file)
            assert cfg, 'ERROR: CONFIG: config file {} is empty!'.format(path)
        for key in cfg.keys():
            setattr(self, key, cfg[key])

    def __args_parser(self):
        args = getattr(self, 'argparse', None)
        if args:
            import argparse
            from pydoc import locate
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
        logger_cfg = getattr(self, 'logger', {'name': self.__class__.__name__})
        if logger_cfg:
            import logging
            self.logger = logging.getLogger(logger_cfg['name'])
            del logger_cfg['name']
            logger_cfg['level'] = logger_cfg.pop('level', 'INFO').upper()
            logger_cfg['format'] = '[%(asctime)s] %(name)s[%(process)d][%(levelname)s]: %(message)s'
            logging.basicConfig(**logger_cfg)