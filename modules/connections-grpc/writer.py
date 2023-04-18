import grpc
import connections_pb2
import connections_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = connections_pb2_grpc.ConnectionsServiceStub(channel)

# Update this with desired payload
item = connections_pb2.ConnectionQuery(
    person=5,
    start_date="2020-01-01",
    end_date="2020-12-30",
    distance=5
)


response = stub.person_contacts(item)
