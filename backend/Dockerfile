FROM python:3.8

EXPOSE 5000

RUN apt-get update -y && apt-get install -y && apt-get autoremove

RUN pip install --upgrade pip

ADD . /sia_storage/backend
WORKDIR /sia_storage/backend

RUN pip install -r requirements.txt
