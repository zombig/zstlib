# -*- coding: utf-8 -*-
"""
Tiny Application

Small Framework for build tiny applications.

"""
import logging
import sys
from weakref import WeakKeyDictionary

from .config import Config
from .config import ConfigHandler


class TinyAppException(Exception):
    """
    Generate general exceptions with provided message and
    outer error (optional).
    """

    def __init__(self, message, errors=None):
        super().__init__(message)
        if errors:
            self.errors = errors


class LoggerConfigHandler(ConfigHandler):
    """
    Update logger configuration on load.
    """

    def __set__(self, instance, value):
        self.default.update(value)
        logging.basicConfig(**self.default)
        super().__set__(instance, self.default)


class TinyAppHandler:
    """
    A default TinyApp class descriptor for create some data handlers (hooks).

    Example:
        Create some child class for store your handler.

        >>> class Example(TinyAppHandler): \\
                def __set__(self, instance, value): \\
                    if not isinctance(value, self.default): \\
                        raise RuntimeError('value shall be string') \\
                    super()__set__(instance, value)
        Then apply this handler to some class param:
        >>> TinyApp.example = Example(str)

        With this example Handler will run every time when something try to
        set Config.example value, and check if this value is str or not.

    """

    def __init__(self, default):
        self.default = default
        self.data = WeakKeyDictionary()
        TinyApp.hooks.append(self.__class__.__name__)

    def __get__(self, instance, owner):
        return self.data.get(instance, self.default)

    def __set__(self, instance, value):
        self.data[instance] = value


class TinyApp:
    """
    A TinnyApp Class

    Build-in params:
        :param configs_class: class that will be used for store app configs.
        :param hooks: storage for keep information about registered hooks.

    Hooks:
        config_class.logger: handler for apply default logger configuration.
    """

    hooks = []

    config_class = Config

    # Logger configuration handler
    config_class.logger = LoggerConfigHandler({
        'level': 'INFO',
        'format': '[%(asctime)s] %(name)s[%(process)d][%(levelname)s]: %(message)s',
    })

    def __init__(self, name):
        """
        :param name: application name.
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.__config = self.config_class()
        self.__config.register_config(name)

        sys.excepthook = self.__excepthook

    def __excepthook(self, *args):
        self.logger.fatal('uncouth exception: %s:', args[1], exc_info=args)

    @property
    def config(self):
        """
        Application's config (view ./config.py)
        """
        return self.__config
