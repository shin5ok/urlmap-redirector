import logging
import sys
from google.cloud.logging.handlers import ContainerEngineHandler

import json

class GCPLog:

    def __init__(self, name: str, mode: str) -> None:
        print(f"mode: {mode}")
        logger = logging.getLogger(name)
        if mode == "gke":
            logger.addHandler(ContainerEngineHandler(name=name, stream=sys.stdout))
        logger.propagate = False
        self.mode = name
        self.mode = mode
        self.logger = logger

    def mode(self, mode: str=""):
        # mode can has a value like gke or run
        if not mode:
            self.mode = mode
        return mode

    def info(self, logdict):
        # self._put("info", logdict)
        logdict["severity"] = "info"
        self.logger.info(json.dumps(logdict))

    def _put(self, level, logdict):
        try:
            self.logger.info(json.dumps(logdict))
        except Exception as e:
            print(str(e))
