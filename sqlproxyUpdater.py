#!/usr/bin/python

import os
import time
import datetime
import MySQLdb
from Updater import *


def main():
    date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    print(date + " Starting updater...")

    db = MySQLdb.connect(host=os.environ['SQLPROXY_HOST'],
                        port=6032,
                        user=os.environ['PROXY_ADMIN_USER'],
                        passwd=os.environ['PROXY_ADMIN_PASS'])
    cur = db.cursor()

    etcd = ETCDClass(os.environ['DISCOVERY_SERVICE'], os.environ['CLUSTER_NAME'])

    while True:
        etcd_sqlnodes = []
        proxydb_sqlnodes = []
        nodeCount = 0
        date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        if os.getenv('DISCOVERY_SERVICE') is None:
            print(date + " DISCOVERY_SERVICE variable is not set")
            continue
        if os.getenv('CLUSTER_NAME') is None:
            print(date + " CLUSTER_NAME variable is not set")
            continue
        print(date + " Reading data from etcd...")
        etcd_sqlnodes = etcd.read()
            
        for node in etcd_sqlnodes:
            cur.execute("SELECT * FROM mysql_servers WHERE hostname = \'" + node + "\'")
            nodeCount = cur.rowcount
            if cur.rowcount is 0:
                print("Adding " + node + " to proxysql")
                cur.execute("INSERT INTO mysql_servers (hostgroup_id, hostname, port, max_replication_lag) VALUES (0, \'" + node + "\', 3306, 20)")
        
        cur.execute("SELECT hostname FROM mysql_servers")
        rows = cur.fetchall()
        nodeCount = cur.rowcount

        for row in rows:
            proxydb_sqlnodes.append(row)
        

        print(date + " ProxySQL is up to date. ProxySQL DB: " + str(nodeCount) + ", ETDC: " + str(len(etcd_sqlnodes)))


        time.sleep(2)

if __name__ == '__main__':
    main()