FROM python:3.7-alpine

#WORKDIR /

COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

EXPOSE 5000

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]