FROM python:3.7-alpine

WORKDIR /persons

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

COPY /modules/persons/requirements.txt /persons/requirements.txt
RUN pip install -r /persons/requirements.txt

EXPOSE 5001

COPY /modules/persons/ /persons/
CMD ["flask", "run", "--host", "0.0.0.0"]