FROM python:3

RUN pip install --no-cache-dir requests

WORKDIR /usr/local/bin
COPY sqlproxyUpdater.py .
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

CMD [ "python", "-u", "./sqlproxyUpdater.py" ]