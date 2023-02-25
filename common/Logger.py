#  Copyright (c) 2023.
import logging

from common.Singleton import Singleton


class Logger(Singleton):

    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)
        return logger
