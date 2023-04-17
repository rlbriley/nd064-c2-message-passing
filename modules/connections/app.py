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
channel = grpc.insecure_channel("localhost:5005")
stub = connections_pb2_grpc.ConnectionsServiceStub(channel)


@app.route("/persons/<person_id>/connection")
@app.param("start_date", "Lower bound of date range", _in="query")
@app.param("end_date", "Upper bound of date range", _in="query")
@app.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
#    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id):
        logger.debug(f"request: {request}")
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)

        connQuery = connections_pb2.ConnectionQuery(
            person_id,
            start_date,
            end_date,
            distance )

        logger.deubg(f"Sending request to gRPC find_contacts({connQuery})")

        results = stub.find_contacts(connQuery)

        logger.deubg(f"Results: {results}")

        return results
