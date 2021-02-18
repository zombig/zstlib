# -*- coding: utf-8 -*-
import json
import socket
import time


class SensuClient:

    OK = 0
    WARNING = 1
    ERROR = 2
    UNKNOWN = 3

    def __init__(
        self, name, address='localhost', port=3030, command='unknown',
        handlers=None,
    ):
        self.name = name
        self.address = address
        self.port = port
        self.handlers = handlers if handlers else ['default']
        self.command = command

    def __send(self, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.address, self.port))
        s.send(message.encode())

    def __compose(self, output, status):
        message = {
            'name': self.name,
            'issued': int(time.time()),
            'output': output.strip(),
            'status': status,
            'command': self.command,
            'handlers': self.handlers,
        }
        return json.dumps(message)

    def ok(self, message=OK):
        self.__send(self.__compose(message, self.OK))

    def warning(self, message):
        self.__send(self.__compose(message, self.WARNING))

    def error(self, message):
        self.__send(self.__compose(message, self.ERROR))

    def unknown(self, message):
        self.__send(self.__compose(message, self.UNKNOWN))
