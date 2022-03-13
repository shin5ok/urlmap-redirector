import signal
import requests
import os
import json

def set_shoutout_when_catching_signal(slack_url: str, json_dict: dict) -> None:
    payload = json.dumps(json_dict)
    def _handler(sig: int, frame) -> None:
        requests.post(slack_url, data=payload)
    signal.signal(signal.SIGTERM, _handler)


if __name__ == '__main__':
    set_shoutout_when_catching_signal(os.environ.get("SLACK_URL"),{"text":"test", "channel":"#kawano"})
    while True:
        pass