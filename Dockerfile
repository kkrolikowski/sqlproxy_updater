FROM ubuntu:18.04

RUN apt-get update && \
    apt-get -y install python3 python3-pip python3-mysqldb && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir requests

WORKDIR /usr/local/bin
COPY *.py /usr/local/bin/

CMD [ "python3", "-u", "./sqlproxyUpdater.py" ]