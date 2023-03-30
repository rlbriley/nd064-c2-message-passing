FROM python:3.7-alpine

WORKDIR /api

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

COPY /modules/api/requirements.txt /api/requirements.txt
RUN pip install -r /api/requirements.txt

EXPOSE 5000

COPY modules/api/ /api/
CMD ["flask", "run", "--host", "0.0.0.0"]