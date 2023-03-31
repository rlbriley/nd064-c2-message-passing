FROM python:3.7-alpine

WORKDIR /locations

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

COPY /modules/locations/requirements.txt /locations/requirements.txt
RUN pip install -r /locations/requirements.txt

EXPOSE 5000

COPY /modules/locations/ /locations/
CMD ["flask", "run", "--host", "0.0.0.0"]