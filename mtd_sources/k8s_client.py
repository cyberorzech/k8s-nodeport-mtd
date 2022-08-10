from loguru import logger
from kubernetes import client, config

class K8s:
    def __init__(self) -> None:
        self.client = self.__check_cluster_connection()
        

    @logger.catch
    def check_resource_existence(self, resource: str) -> bool:
        pass

    @logger.catch
    def check_selector_existence(self, selector: str, resource: str) -> bool:
        pass

    @logger.catch
    def __check_cluster_connection(self):
        try:
            config.load_kube_config()
            # config.load_incluster_config()
            v1 = client.CoreV1Api()
            v1.list_node()
            return v1

        except Exception as e:
            if "Failed to establish a new connection" in str(e):
                return
            else:
                logger.error(f"{e}")
                return


if __name__ == "__main__":
    raise NotImplementedError("Use as class")