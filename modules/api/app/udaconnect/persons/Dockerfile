FROM python:3.7-alpine

WORKDIR /api

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY /modules/api/app/udaconnect/persons/requirements.txt /api/requirements.txt
RUN pip install -r /api/requirements.txt

EXPOSE 5001

COPY /modules/api/app/udaconnect/persons/* /api
CMD ["flask", "run", "--host", "0.0.0.0"]