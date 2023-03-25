FROM python:3.7-alpine

WORKDIR /api

COPY /modules/api/requirements.txt /api/requirements.txt
RUN pip install -r /api/requirements.txt

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

EXPOSE 5000

COPY modules/api/app/ /api/
CMD ["flask", "run", "--host", "0.0.0.0"]