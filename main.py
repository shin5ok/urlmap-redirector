from itertools import groupby
import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import grpc
import sys

from google.cloud import logging
import json
from prometheus_fastapi_instrumentator import Instrumentator
sys.path.append("pb")

import pb.urlmap_pb2_grpc
import pb.urlmap_pb2
import secretm


client = logging.Client()
client.setup_logging()

version: str = "2022061600"

app = FastAPI()

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)


project = os.environ.get("PROJECT")
grpc_host = os.environ.get("URLMAP_API")
if not grpc_host:
    grpc_host = secretm.Secretm(project).get("URLMAP_API")
topic_id = os.environ.get("TOPIC_ID")

channel = grpc.insecure_channel(grpc_host)
stub = pb.urlmap_pb2_grpc.RedirectionStub(channel)


fail_site_path = "/Failure"
import shoutout
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
def get_org(path, request: Request):
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

            src_ip = _get_addr(request)
            logging.info(f"do notify something to {topic_id}")
            message = f"/{path} to {org.org} from {src_ip}"
            data = {"message":message, "notify_to": org.notify_to, "slack_url":org.slack_url, "email": org.email}
            run_notify.Pub(project, topic_id).run(json.dumps(data))
    except Exception as e:
        logging.error(str(e))
        r = f"{fail_site_path}/{path}"
    return RedirectResponse(r)

def _get_addr(request: Request):
    x = request.headers.getlist("X-Forwarded-For")
    ip = "cannot get ip"
    try:
        if x:
            # example
            # 119.229.14.242, 34.102.224.121
            ip = x[0].split(",")[0]
        else:
            ip = request.remote_addr
    except Exception as e:
        logging.error(str(e))
    return ip

if __name__ == "__main__":
    import uvicorn
    port = os.environ.get("PORT", "8080")
    options = {
            'port': int(port),
            'host': '0.0.0.0',
            'workers': 2,
            'reload': True,
        }
    uvicorn.run("main:app", **options)
