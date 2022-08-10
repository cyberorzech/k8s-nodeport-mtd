from loguru import logger
from kubernetes import client, config

@logger.catch
def check_cluster_connection() -> bool:
    try:
        config.load_kube_config()
        # config.load_incluster_config()
        v1 = client.CoreV1Api()
        v1.list_node()
        return True

    except Exception as e:
        if "Failed to establish a new connection" in str(e):
            return False
        else:
            logger.error(f"{e}")
            return False

@logger.catch
def check_resource_existence(resource: str) -> bool:
    pass

if __name__ == "__main__":
    raise NotImplementedError("Use as package")