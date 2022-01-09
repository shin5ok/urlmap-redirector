import logging
import sys
from google.cloud.logging.handlers import ContainerEngineHandler

class GCPLog:

    def init(self, name: str):
        logger = logging.getLogger(name)
        logger.addHandler(ContainerEngineHandler(name=name, stream=sys.stdout))
        logger.propagate = False

    def info(self, logdict):
        pass

    def _put(self, level, logdict):
        pass