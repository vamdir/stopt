FROM python:3.8.12-bullseye

ENV PYTHONUNBUFFERED 1
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN mkdir /app
ADD ./app /app
WORKDIR /app