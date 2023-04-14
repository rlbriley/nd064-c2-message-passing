#!/sur/bin/env python3

import os
import time
from concurrent import futures

import grpc
import connections_pb2
import connections_pb2_grpc
import logging
import psycopg2
import services
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker



DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-grpc-connections")

#Try using SQLAlchemy like the original code.....

url = URL.create(
    drivername="postgresql",
    username=DB_USERNAME,
    password=DB_PASSWORD,
    port=DB_PORT,
    host=DB_HOST,
    database=DB_NAME
)

def get_engine():
    engine = create_engine(url)
    return engine

def get_session():
    engine = get_engine()
    session = sessionmaker(bind=engine)
    return session

#db = SQLAlchemy()
#
# conn = psycopg2.connect(database=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
#conn = psycopg2.connect(database="geoconnections", user="ct_admin", password="wowimsosecure", host="10.98.244.16", port="5432")

class ConnectionsServicer(connections_pb2_grpc.ConnectionsServiceServicer):
    def person_contacts(self, request, context):

        print(f"Request: {request}")
        print(f"Context: {context}")

        result = services.ConnectionService.find_contacts(request.person, request.start_data, request.end_data, request.meters)

        print(f"Result: {result}")

    #     loc = connections_pb2.ConnectionList.ConnectionMsg.LocationMsg()
    #     loc.id = 1234
    #     loc.person_id =  request.person
    #     loc.coordinate = "coordinate"
    #     loc.creation_time = "Creation"
    #     loc._wkt_shape = "SHAPE"

    #     per = connections_pb2.ConnectionList.ConnectionMsg.PersonMsg()
    #     per.id = request.person
    #     per.first_name = "FName"
    #     per.last_name = "LName"
    #     per.company_name = "CName"

    #     connMsg = connections_pb2.ConnectionList.ConnectionMsg(location=loc, person=per)

        connList = connections_pb2.ConnectionList()
        # connList.connections.append(connMsg)

        print(f"Response: {connList}")

        return connList

#     def person_contacts(self, request, context):
#         """
#         Finds all Person who have been within a given distance of a given Person within a date range.

#         This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
#         large datasets. This is by design: what are some ways or techniques to help make this data integrate more
#         smoothly for a better user experience for API consumers?
#         """
#         query = ""
#         if request.person:
#             query = f"SELECT * FROM location WHERE person_id = '{request.person}'"
#             if request.start_date:
#                 query += f" AND creation_time >= '{request.start_date}'"
#                 if request.end_date:
#                     query += f" AND creation_time <= '{request.end_date}'"
#         query += ";"

#         logger.info(f"Query: {query}")

#         cur = conn.cursor()
#         cur.execute(query)
#         rows = cur.fetchall()
#         logger.info(f"All Rows: {rows}")
#         for row in rows:
#             logger.info(f"Next row: {row}")

#         # # Cache all users in memory for quick lookup
#         person_map: dict[int, Person] = {}
#         query = f"SELECT * FROM person"
#         cur.execute(query)
#         rows = cur.fetchall()
#         logger.info(f"All Rows: {rows}")
#         for row in rows:
#             logger.info(f"Next row: {row}")
#             per: Person = Person(row[0], row[1], row[2], row[3])
#             person_map[row[0]] = Person(row[0], row[1], row[2], row[3])


#         # # Prepare arguments for queries
#         # data = []
#         # for location in locations:
#         #     data.append(
#         #         {
#         #             "person_id": person_id,
#         #             "longitude": location.longitude,
#         #             "latitude": location.latitude,
#         #             "meters": meters,
#         #             "start_date": start_date.strftime("%Y-%m-%d"),
#         #             "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
#         #         }
#         #     )

#         query = f"""
#                 SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
#                 FROM    location
#                 WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
#                 AND     person_id != :person_id
#                 AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
#                 AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
#                 """

#         # result: List[Connection] = []
#         # for line in tuple(data):
#         #     for (
#         #         exposed_person_id,
#         #         location_id,
#         #         exposed_lat,
#         #         exposed_long,
#         #         exposed_time,
#         #     ) in db.engine.execute(query, **line):
#         #         location = Location(
#         #             id=location_id,
#         #             person_id=exposed_person_id,
#         #             creation_time=exposed_time,
#         #         )
#         #         location.set_wkt_with_coords(exposed_lat, exposed_long)

#         #         result.append(
#         #             Connection(
#         #                 person=person_map[exposed_person_id], location=location,
#         #             )
#         #         )

#         connList = connections_pb2.ConnectionList()
#         # connList.connections.append(connMsg)

#         logger.info(f"Response: {connList}")

#         return connList

# class Person:
#     def __init__(self, id: int, first_name: str, last_name: str, company_name: str):
#         self.id = id
#         self.first_name = first_name
#         self.last_name = last_name
#         self.company_name = company_name

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
