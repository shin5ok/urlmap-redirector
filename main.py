import os
from flask import Flask
import grpc
import urlmap_pb2

app = Flask(__name__)

@app.route('/ping')
def root():
    return "pong"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
