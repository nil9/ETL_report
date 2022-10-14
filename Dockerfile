FROM python:3.8-slim-buster

WORKDIR /data
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .


