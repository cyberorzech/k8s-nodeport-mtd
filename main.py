from kubernetes import client, config

config.load_kube_config()
# config.load_incluster_config()

v1 = client.CoreV1Api()
nodes = v1.list_node()
print(nodes)
