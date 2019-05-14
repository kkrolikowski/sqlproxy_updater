import requests
import json
import time

class ETCDClass:
    def __init__(self, etcdAddr, clName):
        self.etcdAddr = etcdAddr
        self.clName = clName
        self.nodes = []
    def __del__(self):
        self.nodes = []
    def read(self):
        try:
            etcd = requests.get("http://" + self.etcdAddr + "/v2/keys/pxc-cluster/" + self.clName)
        except requests.exceptions.ConnectionError:
            print("ETCD temporarily unavailable. Backoff engaged. (10s)")
            time.sleep(10)
        else:
            if etcd.status_code == 200:
                etcd_json = json.loads(etcd.text)
                for sqlnodes in etcd_json['node']['nodes']:
                    hosts = sqlnodes['key'].split('/')
                    self.nodes.append(hosts[3])
        return self.nodes
