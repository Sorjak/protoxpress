FROM python:3.12-slim

ENV PYTHONBUFFERED=1

RUN apt update
RUN apt install -y build-essential

RUN pip install uv

ADD ./requirements.txt /requirements.txt
RUN uv pip install --system --no-cache -r requirements.txt

