# syntax=docker/dockerfile:1

FROM python:3.11-slim
RUN apt-get update
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8000
