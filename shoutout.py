import os
import sys
import json
import signal
import requests

def set_shoutout_when_catching_signal(slack_url: str, data_dict: dict) -> None:

    def _handler(sig: int, frame) -> None:
        hostname = _get_where_i_am()
        data_dict["text"] = f"{hostname}:signal {sig}"
        payload = json.dumps(data_dict)
        requests.post(slack_url, data=payload)
        sys.exit(0)

    def _get_where_i_am() -> str:
        metadata_url = "http://169.254.169.254/computeMetadata/v1/instance/hostname"
        try:
            res = requests.get(metadata_url, headers={"Metadata-Flavor":"Google"}, timeout=(0.5,0.5))
            data = res.content
        except Exception as e:
            print(str(e))
            data = os.uname()[1]
        return data

    signal.signal(signal.SIGTERM, _handler)
    signal.signal(signal.SIGINT, _handler)
    signal.signal(signal.SIGHUP, _handler)

if __name__ == '__main__':
    set_shoutout_when_catching_signal(os.environ.get("SLACK_URL"),{"text":"test", "channel":"#kawano"})
    while True:
        pass