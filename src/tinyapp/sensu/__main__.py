# -*- coding: utf-8 -*-
import argparse
from enum import Enum

from . import SensuClient

DEFAULT_HANDLERS = None
DEFAULT_ADDRESS = 'localhost'
DEFAULT_COMMAND = 'unknown'
DEFAULT_PORT = 3030


class Status(Enum):
    ok = 'ok'
    warning = 'warning'
    error = 'error'
    unknown = 'unknown'

    def __str__(self):
        return str(self.value)


def main():
    parser = argparse.ArgumentParser(
        prog='python -m tinyapp.sensu',
        description='Simple Sensu Client',
    )

    parser.add_argument(
        '--name',
        help='Sensu Check Name', required=True,
    )
    parser.add_argument(
        '--address', default=DEFAULT_ADDRESS,
        help='Sensu Client Address (Default "{}")'.format(DEFAULT_ADDRESS),
    )
    parser.add_argument(
        '--port', default=DEFAULT_PORT,
        help='Sensu Client Port (Default "{}")'.format(DEFAULT_PORT),
    )
    parser.add_argument(
        '--command', default=DEFAULT_COMMAND,
        help='Sensu Client Command (Default "{}")'.format(DEFAULT_COMMAND),
    )
    parser.add_argument(
        '--handlers', nargs='*', default=DEFAULT_HANDLERS,
        help='Sensu Helpers List (Default "{}")'.format(DEFAULT_HANDLERS),
    )
    parser.add_argument(
        '-s', '--status', type=Status, choices=list(Status),
        help='Sensu Status', required=True,
    )
    parser.add_argument(
        '-m', '--message',
        help='Sensu Output Message', required=True,
    )
    args = parser.parse_args()

    sensu_client = SensuClient(
        args.name,
        address=args.address,
        port=args.port,
        command=args.command,
        handlers=args.handlers,
    )

    getattr(sensu_client, str(args.status))(args.message)


main()
