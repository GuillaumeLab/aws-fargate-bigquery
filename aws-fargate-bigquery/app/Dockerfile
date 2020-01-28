FROM python:3.7-alpine as server

# Install native libraries, required for numpy
#RUN apk --no-cache add musl-dev linux-headers g++

# Upgrade pip
#RUN pip install --upgrade pip

WORKDIR /server
COPY app.py /server/
COPY requirements.txt /server
RUN pip3 install -r /server/requirements.txt
RUN pip3 install --upgrade google-cloud-bigquery




CMD python3 ./app.py

