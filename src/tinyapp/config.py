# -*- coding: utf-8 -*-
"""
An application's configuration storage.

Load, parse and store configurations as a class attributes.

Please note that loaded options (attrs) can't be deleted.

Example:
    - create several config storages
    >>> c1, c2 = Config().from_dict({'timeout': 10}),\\
                 Config().from_dict({'url': 'https://example.com'})
    >>> print(c1, c2) #  {'timeout': 10} {'url': 'https://example.com'}

    - create additional config and load it from file
    >>> c3 = Config().from_file('./config-example.yaml')
    >>> print(c3) #  {'name': '3rd config'}

    - merge first config with last
    >>> c3.from_config(c1)
    >>> print(c3) #  {'timeout': 10, 'name': '3rd config'}
"""
import yaml


class ConfigException(Exception):
    """
    Generate general exceptions with provided message and
    outer error (optional).
    """

    def __init__(self, message, errors=None):
        super().__init__(message)
        if errors:
            self.errors = errors


class ConfigFileEmpty(ConfigException):
    """
    Config file successfully loaded but has no any content.
    """


class ConfigImmutable(ConfigException):
    """
    Requested config attribute is immutable.
    """


class Config:
    """
    An application's config storage class.

    Build-in params:
        :param configs_storage: global storage for keep info about all class's instances.
                                you can register new instance with-it by call
                                Config.register_config(name) function.
        :param registry: registry for known loaded configuration options (for current
                         instance.

    Pre-defined options:
        :parameter logger: logger configuration.
        :parameter sensu: sensu client configuration.
    """

    configs_storage = {}

    __build_in_attrs = [
        'configs_storage',
        'registry',
    ]

    def __init__(self, allow_overrides=True):
        """
        :param allow_overrides: enable or disable overrides for configuration options.
                                Please note if you disable overrides then you cannot
                                rewrite (update) any config option and get exception
                                instead.
        """
        self.registry = set()
        self.allow_overrides = allow_overrides

        self.logger = {
            'level': 'INFO',
            'format': '[%(asctime)s] %(name)s[%(process)d][%(levelname)s]: %(message)s',
        }

        self.sensu = {}

    def __validate_type(self, value, _type):
        if not isinstance(value, _type):
            raise TypeError(
                '{}: only {} allowed but {} got'.format(
                    self.__class__.__name__, _type, type(value),
                ),
            )

    def __is_immutable(self, value):
        if hasattr(self, value) and not self.allow_overrides:
            raise ConfigImmutable(
                '{}: immutable attr "{}"'.format(
                    self.__class__.__name__, value,
                ),
            )

    def __is_build_in(self, key):
        if key in self.__build_in_attrs:
            raise ConfigException(
                '{}: build-in attr "{}" access denied'.format(
                    self.__class__.__name__, key,
                ),
            )

    def __parse(self, cfg):
        self.__validate_type(cfg, dict)
        for key in cfg.keys():
            setattr(self, key, cfg[key])
            self.registry.add(key)

    def register_config(self, name):
        """
        Register this config instance with-in global configs_storage.
        :param name: name with it configuration will be registered.
        :raise ConfigException: configuration with provided name already
                                exist.
        """
        if self.configs_storage.get(name, False):
            raise ConfigException(
                '{}: config with name "{}" already exist!'.format(
                    self.__class__.__name__, name,
                ),
            )
        self.configs_storage.update({
            name: self,
        })

    def from_dict(self, cfg):
        """
        Wrapper for default config parser.
        :param cfg: dictionary with configuration that will be loaded.
        :return self: config class instance.
        """
        self.__parse(cfg)
        return self

    def from_file(self, path):
        """
        Load configuration from yaml file.
        :param path: path to file.
        :return self: config class instance.
        :raise: ConfigFileEmpty: provided configuration file is empty.
        """
        self.__validate_type(path, str)
        with open(path) as config_file:
            cfg = yaml.safe_load(config_file)
            if not cfg:
                raise ConfigFileEmpty(
                    '{}: config file "{}" is empty'.format(
                        self.__class__.__name__, path,
                    ),
                )
        self.__parse(cfg)
        return self

    def from_config(self, cfg):
        """
        Load configuration from another config's class instance (merge).
        :param cfg: config class instance.
        :return self: config class instance.
        """
        self.__validate_type(cfg, Config)
        for i in cfg.registry:
            self.__parse({i: getattr(cfg, i)})
        return self

    def from_config_storage(self, name):
        """
        Load configuration from configs_storage by name.
        :param name: config name that will be loaded for.
        :return self: config class instance.
        """
        self.__validate_type(name, str)
        self.from_config(
            self.configs_storage[name],
        )
        return self

    def __call__(self, *args, **kwargs):
        """
        Represent loaded options (class attrs) as dictionary.
        :return configs: dictionary with known configuration options.
        """
        configs = {}
        for item in self.registry:
            configs.update({
                item: getattr(self, item),
            })
        return configs

    def __setattr__(self, key, value):
        self.__is_immutable(key)
        super().__setattr__(key, value)

    def __delattr__(self, item):
        """
        Class deleter. Disable any attr deletions.
        :raise ConfigImmutable: you can't delete any class attrs.
        """
        raise ConfigImmutable(
            '{}: unable to remove attr "{}" (immutable)'.format(
                self.__class__.__name__, item,
            ),
        )

    def __str__(self):
        """
        Represent class as a string.
        :return string: loaded (known) config options as a string.
        """
        return str(self())
