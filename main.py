from kubernetes import client, config

# config.load_kube_config()
# # config.load_incluster_config()

# v1 = client.CoreV1Api()
# nodes = v1.list_node()
# print(nodes)

def check_cluster_connection():
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        v1.list_node()
        return True

    except Exception as e:
        if "Failed to establish a new connection" in str(e):
            return False
        else:
            print(str(e))
            return False

def main():
    check_cluster_connection()


if __name__ == "__main__":
    main()