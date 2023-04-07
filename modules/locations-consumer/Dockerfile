FROM python:3.7-alpine

WORKDIR /locations-consumer

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

COPY /modules/locations-consumer/requirements.txt /locations-consumer/requirements.txt
RUN pip install -r /locations-consumer/requirements.txt

EXPOSE 5000

COPY /modules/locations-consumer/ /locations-consumer/
CMD ["python3", "wsgi.py"]
# CMD ["flask", "run", "--host", "0.0.0.0"]