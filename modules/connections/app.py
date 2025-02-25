#!/sur/bin/env python3
from flask import Flask, jsonify, json, request
from flask import request
from flask_cors import CORS
from flask_restx import Namespace, Resource

import time
from concurrent import futures

import grpc
import connections_pb2
import connections_pb2_grpc
import logging
import re

DATE_FORMAT = "%Y-%m-%d"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("connections")

# Define the Flask application
app = Flask(__name__)
cors = CORS(app, resources=r'/api/*')

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

    def __str__(self):
        return json.dumps(self)

class person_out(dict):
    def __init__(self, person):
        self['id'] = person.id
        self['first_name'] = person.first_name
        self['last_name'] = person.last_name
        self['company_name'] = person.company_name

class loc_per(dict):
    def __init__(self, loc: location_out, person: person_out):
        self['location'] = loc
        self['person'] = person

    def __str__(self):
        return json.dumps(self)

class connections_out:
    def __init__(self):
        self.connections = []

    def add(self, loc: location_out, person: person_out):
        self.connections.append(loc_per(loc, person))

def connlist_to_json(connection_list):
    connections = connection_list.connections
    contact_cnt = len(connections)
    logger.debug(f"Contact count: {contact_cnt}")
    if contact_cnt > 0:
        logger.debug(f"connections[0].location: {connections[0].location}")
        logger.debug(f"connections[0].person: {connections[0].person}")

    conn_list = connections_out()
    for conn in connections:
        l = conn.location
        # get the latitude (la) and longitue (lo) from the wkt_shape
        pattern_text = r'ST_POINT\(([-\d\.]+)\s+([-\d\.]+)\)'
        pattern = re.compile(pattern_text)
        shape = conn.location._wkt_shape
        match = pattern.match(shape)
        la = match.group(1)
        lo = match.group(2)

        # Convert from location message to location_out dict object
        l1 = location_out(l.id, l.person_id, conn.location.creation_time, lo, la)
        # Convert conn.person to person_out dict object
        p1 = person_out(conn.person)

        conn_list.add(l1, p1)

        logger.debug(f"location_out: {json.dumps(l1)}")
        logger.debug(f"person_out: {json.dumps(p1)}")

    logger.debug(f"connList: {conn_list.connections}")

    json_str = json.dumps(conn_list.connections)

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

    logger.debug(f"gRPC response from find_contacts: {connQuery}")

    connections = stub.person_contacts(connQuery)

    logger.debug(f"Connections: {connections}")

    # convert from ConnectionList to JSON
    conn_list = connlist_to_json( connections )

    response = app.response_class(
        response = conn_list,
        status = 200,
        mimetype = 'application/json'
    )

    return response


# health REST route.
# Will return "OK - healthy" if the application is running
@app.route("/health")
def health():
    '''
    health REST route.
    Will return "OK - healthy" if the application is running
    '''
    response = app.response_class(
        response = json.dumps({"result": "OK - healthy"}),
        status = 200,
        mimetype = 'application/json'
    )
    logger.info('healthz request successful response=%s',
             json.dumps(response.json))
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
