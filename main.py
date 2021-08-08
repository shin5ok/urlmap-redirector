import os
from flask import Flask, redirect
import grpc
import sys
sys.path.append("pb")
import pb.urlmap_pb2_grpc
import pb.urlmap_pb2

app = Flask(__name__)

grpc_host = os.environ.get('GRPC_HOST', 'localhost:8080')

@app.route('/Ping')
def root():
    return "Pong"

@app.route('/<path>')
def get_org(path):
	channel = grpc.insecure_channel(grpc_host)
	stub = pb.urlmap_pb2_grpc.RedirectionStub(channel)
	req = pb.urlmap_pb2.RedirectPath(path=path)
	org = stub.GetOrgByPath(req)
	print(f"/{path} > {org.org}")
	return redirect(org.org)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))


