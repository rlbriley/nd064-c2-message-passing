FROM python:3.7-alpine

WORKDIR /connections-grpc

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

COPY modules/connections-grpc/requirements.txt /connections-grpc/requirements.txt
RUN pip install -r /connections-grpc/requirements.txt

EXPOSE 5000,5005

COPY modules/connections-grpc/ /connections-grpc/
CMD ["python3", "grpcConnections.py"]