import os
from flask import Flask, redirect
import grpc
import sys

import google.cloud.logging
import logging

sys.path.append("pb")

import pb.urlmap_pb2_grpc
import pb.urlmap_pb2

import secretm

client = google.cloud.logging.Client()
client.setup_logging()

logging.basicConfig(level=logging.INFO)


app = Flask(__name__)

project = os.environ.get("PROJECT")
grpc_host = os.environ.get("URLMAP_API")
if not grpc_host:
    grpc_host = secretm.Secretm(project).get("URLMAP_API")
topic_id = os.environ.get("TOPIC_ID")

channel = grpc.insecure_channel(grpc_host)
stub = pb.urlmap_pb2_grpc.RedirectionStub(channel)

version = "2022010301"

fail_site_path = "/Failure"

# reserve path 'Ping'
@app.route("/")
@app.route("/Ping")
def _ping():
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
        if not org.org:
            raise Exception(f"no any record for /{path}")
        r = org.org
        if topic_id and org.notify_to:
            import run_notify

            logging.info(f"do notify something to {topic_id}")
            run_notify.Pub(project, topic_id).run(org.notify_to)
    except Exception as e:
        logging.error(str(e))
        r = f"{fail_site_path}/{path}"
    return redirect(r)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
