import requests
import json

class ETCDClass:
    nodes = []

    def __init__(self, etcdAddr, clName):
        self.etcdAddr = etcdAddr
        self.clName = clName
    def read(self):
        etcd = requests.get("http://" + self.etcdAddr + "/v2/keys/pxc-cluster/" + self.clName)
        if etcd.status_code == 200:
            etcd_json = json.loads(etcd.text)
            for nodes in etcd_json['node']['nodes']:
                hosts = nodes['key'].split('/')
                nodes.append(hosts[3])
