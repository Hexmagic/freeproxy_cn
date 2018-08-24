import logzero
from logzero import logger
import logging
import traceback

__all__ = ('logger', 'get_trace')
logzero.logfile("app.log", maxBytes=1e6, backupCount=3,
                loglevel=logging.WARNING)


def get_trace():
    return traceback.format_exc()
