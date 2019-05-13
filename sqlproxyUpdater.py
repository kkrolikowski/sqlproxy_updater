#!/usr/bin/python

import requests
import json
import os
import time
import datetime
import MySQLdb


date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
print(date + " Starting updater...")

db = MySQLdb.connect(host=os.environ['SQLPROXY_HOST'],
                    port=6032,
                    user=os.environ['PROXY_ADMIN_USER'],
                    passwd=os.environ['PROXY_ADMIN_PASS'])
cur = db.cursor()

while True:
    etcd_sqlnodes = []
    nodeCount = 0
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
            etcd_sqlnodes.append(hosts[3])
        
        for node in etcd_sqlnodes:
            cur.execute("SELECT * FROM mysql_servers WHERE hostname = \'" + node + "\'")
            cur.fetchall()
            nodeCount = cur.rowcount
            if cur.rowcount is 0:
                print("Adding " + node + " to proxysql")
                cur.execute("INSERT INTO mysql_servers (hostgroup_id, hostname, port, max_replication_lag) VALUES (0, \'" + node + "\', 3306, 20)")

        print(date, + " ProxySQL is up to date. ProxySQL DB: " + str(nodeCount) + ", ETDC: " + str(len(etcd_sqlnodes)))

    else:
        print(date + " ERROR connecting to etcd")
    time.sleep(2)