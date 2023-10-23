import datetime as dt
from enum import StrEnum, Enum


class ConsoleColor(StrEnum):
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    white = "\x1b[37m"
    bold = "\x1b[1m"
    reset = "\x1b[0m"


class LoggingLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    CRITICAL = 4


class Logger:

    def __init__(self, name):
        self.name = name

    @staticmethod
    def _get_datetime() -> str:
        x = dt.datetime.now()
        return f"[{str(x.year)[2:]}-{x.month}-{x.day} {x.hour}:{x.minute}:{x.second}] :: "

    def debug(self, content: str):
        print(ConsoleColor.blue + Logger._get_datetime() +
              f"[{self.name}] :: [DEBUG] :: " + content + ConsoleColor.reset)

    def info(self, content: str):
        print(ConsoleColor.green + Logger._get_datetime() +
              f"[{self.name}] :: [INFO] :: " + content + ConsoleColor.reset)

    def warn(self, content: str):
        print(ConsoleColor.yellow + Logger._get_datetime() +
              f"[{self.name}] :: [WARN] :: " + content + ConsoleColor.reset)

    def error(self, content: str):
        print(ConsoleColor.red + Logger._get_datetime() +
              f"[{self.name}] :: [ERROR] :: " + content + ConsoleColor.reset)

    def critical(self, content: str):
        print(ConsoleColor.red + ConsoleColor.bold + Logger._get_datetime() +
              f"[{self.name}] :: [CRITICAL] :: " + content + ConsoleColor.reset)

    @staticmethod
    def logger_test(msg: str):
        logger = Logger("TEST")
        logger.info(msg)
        logger.debug(msg)
        logger.warn(msg)
        logger.error(msg)
        logger.critical(msg)
