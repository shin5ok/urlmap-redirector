import os
from flask import Flask, redirect
import grpc
import sys
sys.path.append("pb")
import pb.urlmap_pb2_grpc
import pb.urlmap_pb2

app = Flask(__name__)

grpc_host = os.environ.get('GRPC_HOST', 'localhost:8080')

fail_site_path = "/Failure"

# reserve string 'Ping'
@app.route('/Ping')
def _root():
    return "Pong"

@app.route(f'/{fail_site_path}/<path>')
def _fail(path):
    return f"Not Found /{path}"

@app.route('/<path>')
def get_org(path):
    channel = grpc.insecure_channel(grpc_host)
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


