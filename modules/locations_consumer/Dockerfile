FROM python:3.7-alpine

WORKDIR /locations_consumer

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

COPY /modules/locations_consumer/requirements.txt /locations_consumer/requirements.txt
RUN pip install -r /locations_consumer/requirements.txt

EXPOSE 5000

COPY /modules/locations_consumer/ /locations_consumer/
CMD ["flask", "run", "--host", "0.0.0.0"]