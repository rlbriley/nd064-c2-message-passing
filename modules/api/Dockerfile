FROM python:3.7-alpine

WORKDIR /app

COPY CODEOWNERS /app/CODEOWNERS
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

EXPOSE 5000

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]