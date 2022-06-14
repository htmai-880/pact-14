FROM python:3.7-slim

LABEL name="s2r-backend" \
      version="0.1"

EXPOSE 80
CMD python main.py

RUN mkdir /server
WORKDIR /server

COPY ./requirements.txt /server/requirements.txt
RUN pip install -r requirements.txt

COPY ./ /server/
