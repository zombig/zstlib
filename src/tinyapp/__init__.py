# -*- coding: utf-8 -*-
"""
TinyApp

Small Framework for build any kind of applications.

Features:
    - Store application configuration.
    - Load application configuration from yaml file, dict or merge with.
      another instance.
    - build-in logger with small pre-defined config.
    - ask arguments with CLI (i.e. app config file)
    - Hooks/Handlers for config entries or app methods.

Todo:
    - alerting with sensu.
    - alerting for ERROR/CRITICAL/FATAL log events.
    - send stats with statsd client
    - send error metrics for ERROR/CRITICAL/FATAL log events.
    - configuration schemes and validators
"""
from .app import TinyApp
from .app import TinyAppHandler
from .cli import cli_config_file
from .cli import parse_args
from .config import Config
from .config import ConfigHandler
from .sensu import SensuClient

__all__ = [
    'TinyApp',
    'TinyAppHandler',
    'Config',
    'ConfigHandler',
    'SensuClient',
    'parse_args',
    'cli_config_file',
]
