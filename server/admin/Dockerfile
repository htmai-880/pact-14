FROM python:3.8-slim

LABEL name="s2r-admin" \
      version="0.1"

CMD python main.py

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./app/ /app/
