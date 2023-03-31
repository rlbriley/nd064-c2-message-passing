FROM python:3.7-alpine

WORKDIR /connections

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

COPY /modules/connections/requirements.txt /connections/requirements.txt
RUN pip install -r /connections/requirements.txt

EXPOSE 5000

COPY modules/connections/ /connections/
CMD ["flask", "run", "--host", "0.0.0.0"]