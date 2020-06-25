# -*- coding: utf-8 -*-
"""
Tiny Application

Implement config storage, logging and sensu alerting.
"""
import logging

from .config import Config
from .sensu_client import SensuClient


class TinyAppException(Exception):
    """
    Generate general exceptions with provided message and
    outer error (optional).
    """

    def __init__(self, message, errors=None):
        super().__init__(message)
        if errors:
            self.errors = errors


class TinyApp:
    """
    A TinnyApp Class

    Build-in params:
        :param configs_class: class that will be used for store app configs.
    """
    config_class = Config

    def __init__(self, name):
        """
        :param name: application name.
        """

        self.__sensu = None
        self.__logger = None

        self.name = name
        self.__config = self.config_class()
        self.__config.register_config(name)

    @property
    def logger(self):
        """
        Application's logger (view python logging).
        """
        if not self.__logger:
            logging.basicConfig(**self.config.logger)
            self.__logger = logging.getLogger(self.name)
        return self.__logger

    @property
    def sensu(self):
        """
        Application's Sensu client (view ./sensu_client.py).
        """
        if not self.__sensu:
            if self.config.sensu:
                self.__sensu = SensuClient(**self.config.sensu)
        return self.__sensu

    @property
    def config(self):
        """
        Application's config (view ./config.py)
        """
        return self.__config
