#!/sur/bin/env python3

import time
import re
import json
from concurrent import futures

import grpc
import connections_pb2
import connections_pb2_grpc
import logging
from datetime import datetime, date
from services import ConnectionService


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("grpc-connections")

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

class ConnectionsServicer(connections_pb2_grpc.ConnectionsServiceServicer):
    def person_contacts(self, request, context):

        logger.info(f"Request: {request}")

        sdate: datetime = date.fromisoformat(request.start_date)
        edate: datetime = date.fromisoformat(request.end_date)
        result = ConnectionService.find_contacts(request.person, sdate, edate, request.distance)

        connList = connections_pb2.ConnectionList()
        for conn in result:
            logger.debug( f"conn: {conn}")

            loc = connections_pb2.ConnectionList.ConnectionMsg.LocationMsg()
            loc.id = conn.location.id
            loc.person_id =  conn.location.person_id
            if conn.location.coordinate:
                loc.coordinate = conn.location.coordinate
            loc.creation_time = conn.location.creation_time.isoformat()
            loc._wkt_shape = conn.location._wkt_shape

            per = connections_pb2.ConnectionList.ConnectionMsg.PersonMsg()
            per.id = conn.person.id
            per.first_name = conn.person.first_name
            per.last_name = conn.person.last_name
            per.company_name = conn.person.company_name

            connMsg = connections_pb2.ConnectionList.ConnectionMsg(location=loc, person=per)

            connList.connections.append(connMsg)

            # l = conn.location
            # pattern_text = r'ST_POINT\(([-\d\.]+)\s+([-\d\.]+)\)'
            # pattern = re.compile(pattern_text)
            # shape = conn.location._wkt_shape
            # logger.debug(f"shape: {shape}")
            # match = pattern.match(shape)
            # lo = match.group(1)
            # la = match.group(2)

            # l1 = location_out(l.id, l.person_id, conn.location.creation_time, lo, la)
            # logger.debug(f"location_out: {location_out}")
            # conn_list1.add(l1, conn.person)

        # logger.debug(f"Response: {connList}")

        # ooo = json.dumps(conn_list1)
        logger.debug(f"New Response: \n{connList}")

        return connList

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
connections_pb2_grpc.add_ConnectionsServiceServicer_to_server(ConnectionsServicer(), server)


logger.info("Server starting on port 5005...")

server.add_insecure_port("[::]:5005")
logger.debug(f"Server: {server}")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
