

import logging
import json


class JSONLogger:
    def __init__(self, name="agent"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

    def log(self, event: str, data: dict):
        payload = {
            "event": event,
            "data": data
        }
        self.logger.info(json.dumps(payload))