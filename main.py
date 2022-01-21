import os
from flask import Flask, redirect, request
import grpc
import sys

import google.cloud.logging
import logging
import json

sys.path.append("pb")

import pb.urlmap_pb2_grpc
import pb.urlmap_pb2

import secretm

client = google.cloud.logging.Client()
client.setup_logging()

app = Flask(__name__)

project = os.environ.get("PROJECT")
grpc_host = os.environ.get("URLMAP_API")
if not grpc_host:
    grpc_host = secretm.Secretm(project).get("URLMAP_API")
topic_id = os.environ.get("TOPIC_ID")

channel = grpc.insecure_channel(grpc_host)
stub = pb.urlmap_pb2_grpc.RedirectionStub(channel)

version = "2022012000"

fail_site_path = "/Failure"

# reserve path 'Ping'
@app.route("/")
@app.route("/Ping")
def _ping():
    logging.info("access to /")
    return f"Pong on {version}"


@app.route(f"/{fail_site_path}/<path>")
def _fail(path):
    contents = f"Not Found /{path}"
    return contents


@app.route("/<path>")
def get_org(path):
    logging.info(f"try to connect to {grpc_host}")
    try:
        req = pb.urlmap_pb2.RedirectPath(path=path)
        org = stub.GetOrgByPath(req)
        logging.info(f"return value is {org}")
        logging.info(f"/{path} > {org.org}")
        r = org.org
        if not r:
            raise Exception(f"no any record for /{path}")
        if topic_id and org.notify_to:
            import run_notify

            src_ip = _get_addr()
            logging.info(f"do notify something to {topic_id}")
            message = f"/{path} to {org.org} from {src_ip}"
            data = {"message":message, "notify_to": org.notify_to, "slack_url":org.slack_url, "email": org.email}
            run_notify.Pub(project, topic_id).run(json.dumps(data))
    except Exception as e:
        logging.error(str(e))
        r = f"{fail_site_path}/{path}"
    return redirect(r)

def _get_addr():
    x = request.headers.getlist("X-Forwarded-For")
    ip = "cannot get ip"
    try:
        if x:
            # example
            # 119.229.14.242, 34.102.224.121
            ip = x[0].split(",")[0]
        else:
            ip = request.remote_addr
    except:
        pass
    return ip

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
