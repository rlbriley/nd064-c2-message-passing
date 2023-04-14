#!/sur/bin/env python3

import os
import time
from concurrent import futures

import grpc
import connections_pb2
import connections_pb2_grpc
import logging
import psycopg2
from datetime import datetime, date
from services import ConnectionService


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("grpc-connections")

class ConnectionsServicer(connections_pb2_grpc.ConnectionsServiceServicer):
    def person_contacts(self, request, context):

        logger.info(f"Request: {request}")
        logger.info(f"Context: {context}")

        # result = ConnectionService.find_contacts(request.person, datetime.fromisoformat(request.start_date), datetime.fromisoformat(request.end_date), request.distance)
        sdate: datetime = date.fromisoformat(request.start_date)
        edate: datetime = date.fromisoformat(request.end_date)
        result = ConnectionService.find_contacts(request.person, sdate, edate, request.distance)

#        logger.info(f"Result: {result}")

        connList = connections_pb2.ConnectionList()
        for conn in result:
            logger.debug( f"conn: {conn}")

            loc = connections_pb2.ConnectionList.ConnectionMsg.LocationMsg()
            loc.id = conn.location.id
            loc.person_id =  conn.location.person_id
            if conn.location.coordinate:
                loc.coordinate = conn.location.coordinate
            loc.creation_time = conn.location.creation_time
            loc._wkt_shape = conn.location._wkt_shape

            per = connections_pb2.ConnectionList.ConnectionMsg.PersonMsg()
            per.id = conn.person.id
            per.first_name = conn.person.first_name
            per.last_name = conn.person.last_name
            per.company_name = conn.person.company_name

            connMsg = connections_pb2.ConnectionList.ConnectionMsg(location=loc, person=per)

            connList.connections.append(connMsg)

        logger.info(f"Response: {connList}")

        return connList


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
connections_pb2_grpc.add_ConnectionsServiceServicer_to_server(ConnectionsServicer(), server)


logger.info("Server starting on port 5005...")

server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
