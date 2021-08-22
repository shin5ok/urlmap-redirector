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

project = os.environ.get('PROJECT')
grpc_host = os.environ.get('URLMAP_API')
if not grpc_host:
    grpc_host = secretm.Secretm(project).get("URLMAP_API")

channel = grpc.insecure_channel(grpc_host)
stub = pb.urlmap_pb2_grpc.RedirectionStub(channel)

fail_site_path = "/Failure"

logging.basicConfig(level=logging.INFO)

# reserve string 'Ping'
@app.route('/')
@app.route('/Ping')
def _ping():
    return "Pong"

@app.route(f'/{fail_site_path}/<path>')
def _fail(path):
    contents = f"Not Found /{path}"
    return contents

@app.route('/<path>')
def get_org(path):
    logging.info(f"connecting to {grpc_host}")
    try:
        req = pb.urlmap_pb2.RedirectPath(path=path)
        org = stub.GetOrgByPath(req)
        print(f"/{path} > {org.org}")
        print(org)
        if not org.org:
            raise Exception("no record")
        r = org.org
    except Exception as e:
        print(e)
        r = f"{fail_site_path}/{path}"
    return redirect(r)

def notify():
	pass

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))


