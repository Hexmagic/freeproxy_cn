import logzero
from logzero import logger
import logging

logzero.logfile("app.log", maxBytes=1e6, backupCount=3,
                loglevel=logging.WARNING)