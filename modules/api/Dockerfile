FROM python:3.7-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
RUN echo `pwd`
RUN echo `ls -la`
COPY requirements.txt /app
RUN echo `ls -la /app`
RUN pip install -r /app/requirements.txt

EXPOSE 5000

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]