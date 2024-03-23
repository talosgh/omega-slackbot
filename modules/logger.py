import logging
import sys


class Logger:
    def __init__(self, app_config):
        self.app_config = app_config
        self.fmt = self.app_config.fmt
        self.level = self.app_config.level
        self.dfmt = self.app_config.dfmt

    def get_logger(self):
        try:
            formatter = logging.Formatter(
                fmt=self.fmt,
                datefmt=self.dfmt,
            )
            handler = logging.StreamHandler(sys.stdout)
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(self.level)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        except Exception as e:
            sys.exit(f"Error setting up logging: {e}")

        return self.logger
