#!/sur/bin/env python3
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List
from werkzeug.exceptions import abort
from google.protobuf.json_format import MessageToJson, MessageToDict

import time
from concurrent import futures

import grpc
import connections_pb2
import connections_pb2_grpc
import logging
import re
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

class location_out(dict):
    # Constructor
    def __init__(self, id, pid, ctime, lo, la):
        self['id'] = id
        self['person_id'] = pid
        self['creation_time'] = ctime
        self['longitude'] = lo
        self['latitude'] = la

class loc_per(dict):
    def __init__(self, loc, person):
        self['location'] = loc
        self['person'] = person

class connections_out:
    def __init__(self):
        self.connections = []

    def add(self, loc, person):
        self.connections.append(loc_per(loc, person))

def connlist_to_json(connection_list):
    connections = connection_list.connections
    contact_cnt = len(connections)
    logger.debug(f"Contact count: {contact_cnt}")
    logger.debug(f"connections[0].location: {connections[0].location}")
    logger.debug(f"connections[0].person: {connections[0].person}")

    conn_list = connections_out()
    for conn in connections:
        l = conn.location
        pattern_text = r'ST_POINT\(([-\d\.]+)\s+([-\d\.]+)\)'
        pattern = re.compile(pattern_text)
        shape = conn.location._wkt_shape
        logger.debug(f"shape: {shape}")
        match = pattern.match(shape)
        lo = match.group(1)
        la = match.group(2)

        l1 = location_out(l.id, l.person_id, conn.location.creation_time, lo, la)
        logger.debug(f"location_out: {location_out}")
        conn_list.add(l1, conn.person)

    logger.debug(f"connList: {conn_list}")

    json_str = json.dumps(conn_list)
    return json_str

@app.route("/api/persons/<person_id>/connection", methods = ['GET'])
def get(person_id):
    logger.debug(f"request: {request}")
    sdate: str = request.args["start_date"]
    edate: str = request.args["end_date"]
    dist = request.args.get("distance", 5, type=int)

    connQuery = connections_pb2.ConnectionQuery(
        person=int(person_id),
        start_date=sdate,
        end_date=edate,
        distance=dist )

    logger.debug(f"Sending request to gRPC find_contacts({connQuery})")

    contacts = stub.person_contacts(connQuery)

    logger.debug(f"Contacts: {contacts}")

    # todo convert from ConnectionList to JSON
    conn_list = connlist_to_json( contacts )

    results: str = json.dumps(conn_list)

    logger.debug(f"results: {results}")

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
