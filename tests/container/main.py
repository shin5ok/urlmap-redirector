import os
from flask import Flask, redirect
import mygcplogging

app = Flask(__name__)

logging = mygcplogging.GCPLog(__name__, "gke")

@app.route('/')
@app.route('/Ping')
def _ping():
    version = os.environ.get("VERION", "0.01")
    logging.info({"severity":"info","path":"/","tako":"ika"})
    return f"Pong on {version}"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

