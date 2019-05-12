#!/usr/bin/python

import requests
import json
import os
import time
import datetime

date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
print(date + " Starting updater...")

while True:
    date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    if os.getenv('DISCOVERY_SERVICE') is None:
        print(date + " DISCOVERY_SERVICE variable is not set")
        continue
    if os.getenv('CLUSTER_NAME') is None:
        print(date + " CLUSTER_NAME variable is not set")
        continue
    print(date + " Reading data from etcd...")
    etcd = requests.get("http://" + os.environ['DISCOVERY_SERVICE'] + "/v2/keys/pxc-cluster/" + os.environ['CLUSTER_NAME'])

    if etcd.status_code == 200:
        etcd_json = json.loads(etcd.text)
        for nodes in etcd_json['node']['nodes']:
            hosts = nodes['key'].split('/')
            print(hosts[3])

    else:
        print(date + " ERROR connecting to etcd")
    time.sleep(2)