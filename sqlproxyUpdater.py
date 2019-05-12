#!/usr/bin/python

import requests
import json
import os
import time

print("Starting updater...")

while True:
    if os.environ['DISCOVERY_SERVICE'] is None:
        print("DISCOVERY_SERVICE variable is not set")
        continue
    if os.environ['CLUSTER_NAME'] is None:
        print("CLUSTER_NAME variable is not set")
    continue
    print("Reading data from etcd...")
    etcd = requests.get("http://" + os.environ['DISCOVERY_SERVICE'] + "/v2/keys/pxc-cluster/" + os.environ['CLUSTER_NAME'])

    if etcd.status_code == 200:
        etcd_json = json.loads(etcd.text)
        for nodes in etcd_json['node']['nodes']:
            hosts = nodes['key'].split('/')
            print(hosts[3])

    else:
        print("ERROR connecting to etcd")
    time.sleep(2)