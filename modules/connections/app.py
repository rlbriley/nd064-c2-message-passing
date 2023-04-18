#!/sur/bin/env python3
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List
from werkzeug.exceptions import abort

import time
from concurrent import futures

import grpc
import connections_pb2
import connections_pb2_grpc
import logging
from marshmallow import Schema, fields
from datetime import datetime, date
from services import ConnectionService

DATE_FORMAT = "%Y-%m-%d"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("connections")

# Define the Flask application
app = Flask(__name__)

print("Sending sample payload...")

# Create stub to send gRPC message.
channel = grpc.insecure_channel("grpc-connections.default.svc.cluster.local:5005")
stub = connections_pb2_grpc.ConnectionsServiceStub(channel)


@app.route("/api/persons/<person_id>/connection", methods = ['GET'])
def get(person_id):
    logger.debug(f"request: {request}")
    sdate: str = request.args["start_date"]
    edate: str = request.args["end_date"]
    dist = request.args.get("distance", 5, type=int)

    logger.debug(f"distance: {dist}")

    connQuery = connections_pb2.ConnectionQuery(
        person=int(person_id),
        start_date=sdate,
        end_date=edate,
        distance=dist )

    logger.debug(f"Sending request to gRPC find_contacts({connQuery})")

    results = stub.person_contacts(connQuery)

    logger.debug(f"Results: {results}")

    return results

# health REST route.
# Will return "OK - healthy" if the application is running
@app.route("/health")
def health():
    '''
    health REST route.
    Will return "OK - healthy" if the application is running
    '''
    response = app.response_class(
        response=json.dumps({"result": "OK - healthy"}),
        status=200,
        mimetype='application/json'
    )
    logger.info('healthz request successful response=%s',
             json.dumps(response.json))
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
