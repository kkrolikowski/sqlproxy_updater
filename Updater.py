import requests
import json

class ETCDClass:
    def __init__(self, etcdAddr, clName):
        self.etcdAddr = etcdAddr
        self.clName = clName
        self.nodes = []
    def __del__(self):
        self.nodes = []
    def read(self):
        etcd = requests.get("http://" + self.etcdAddr + "/v2/keys/pxc-cluster/" + self.clName)
        if etcd.status_code == 200:
            etcd_json = json.loads(etcd.text)
            for sqlnodes in etcd_json['node']['nodes']:
                hosts = sqlnodes['key'].split('/')
                self.nodes.append(hosts[3])
        return self.nodes
