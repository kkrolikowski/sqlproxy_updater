FROM ubuntu:18.04

RUN apt-get update && \
    apt-get -y install python python-pip && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir requests

WORKDIR /usr/local/bin
COPY ./sqlproxyUpdater.py .
#COPY ./entrypoint.sh /entrypoint.sh

#RUN chmod +x /entrypoint.sh
#ENTRYPOINT [ "/entrypoint.sh" ]

CMD [ "python", "-u", "./sqlproxyUpdater.py" ]