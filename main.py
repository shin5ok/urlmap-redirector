import os
from flask import Flask, redirect
import grpc
import sys
import logging
sys.path.append("pb")
import pb.urlmap_pb2_grpc
import pb.urlmap_pb2

import secretm

app = Flask(__name__)

grpc_host = os.environ.get('URLMAP_API')
project = os.environ.get('PROJECT')
if not grpc_host:
    grpc_host = secretm.Secretm(project).get("URLMAP_API")
channel = grpc.insecure_channel(grpc_host)

fail_site_path = "/Failure"

logging.basicConfig(level=logging.INFO)

# reserve string 'Ping'
@app.route('/')
@app.route('/Ping')
def _ping():
    return "Pong"

@app.route(f'/{fail_site_path}/<path>')
def _fail(path):
    path = f"Not Found /{path}"
    logging.warning(path)
    new_path = f'/{fail_site_path}/{path}'
    return redirect(new_path)

@app.route('/<path>')
def get_org(path):
    logging.info(f"connecting to {grpc_host}")
    try:
        stub = pb.urlmap_pb2_grpc.RedirectionStub(channel)
        req = pb.urlmap_pb2.RedirectPath(path=path)
        org = stub.GetOrgByPath(req)
        print(f"/{path} > {org.org}")
        r = org.org
    except Exception as e:
        print(e)
        r = f"{fail_site_path}/{path}"
    return redirect(r)

def notify():
	pass

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))


