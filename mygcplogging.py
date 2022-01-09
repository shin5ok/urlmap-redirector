import logging
import sys
from google.cloud.logging.handlers import ContainerEngineHandler

def init(name: str):
    logger = logging.getLogger(name)
    logger.addHandler(ContainerEngineHandler(name=name, stream=sys.stdout))
    logger.propagate = False
    return logger
