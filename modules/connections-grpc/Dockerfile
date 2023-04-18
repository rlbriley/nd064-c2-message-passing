FROM python:3.7-alpine

WORKDIR /connections_grpc

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

COPY modules/connections_grpc/requirements.txt /connections_grpc/requirements.txt
RUN pip install -r /connections_grpc/requirements.txt

EXPOSE 5000,5005

COPY modules/connections_grpc/ /connections_grpc/
CMD ["python3", "grpcConnections.py"]