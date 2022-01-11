import os
from flask import Flask, redirect
import mygcplogging
import google.cloud.logging
import logging
client = google.cloud.logging.Client()
client.setup_logging()


app = Flask(__name__)

MODE = os.environ.get("MODE", "gcp")
# gcplog = mygcplogging.GCPLog(__name__, MODE)

@app.route('/')
def _ping():
    version = os.environ.get("VERION", "0.01")
    logdict = {"path":"/","tako":"ika"}
    logging.info(logdict)
    logging.warning(logdict)
    logging.error(logdict)
    return f"Pong on {version}"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
