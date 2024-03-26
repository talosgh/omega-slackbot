# logger.py

import logging
from logging.handlers import RotatingFileHandler
import os


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AppLogger(metaclass=SingletonType):
    def __init__(self):
        # Create a logger with 'AppLogger' as the base name
        self.logger = logging.getLogger("OMEGA")
        # Set the default logging level to DEBUG
        self.logger.setLevel(logging.DEBUG)  # Ensures debug and above are logged

        # Define the format for the log messages
        formatter = logging.Formatter(
            "%(asctime)s %(name)-5s %(levelname)+8s: %(message)s"
        )

        # Ensure the 'logs' directory exists
        if not os.path.exists("logs"):
            os.makedirs("logs")

        # Create a rotating file handler
        file_handler = RotatingFileHandler(
            "logs/application.log", maxBytes=1 * 1024 * 1024, backupCount=5
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Create a console handler for output to stdout
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self, name=None):
        # If a name is provided, get a child logger with that name
        # Otherwise, return the base logger
        if name:
            return self.logger.getChild(name)
        return self.logger


# Function to be used by main application and modules for getting a logger
def get_logger(name=None):
    return AppLogger().get_logger(name=name)
