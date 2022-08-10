import resource
from loguru import logger
from kubernetes import client, config

class K8s:
    def __init__(self) -> None:
        self.client = self.__check_cluster_connection()
        

    @logger.catch
    def check_resource_existence(self, resource_name: str, resource_type: str) -> bool:
        try:
            if not isinstance(resource_name, str) or not isinstance(resource_type, str):
                raise TypeError(f"Arguments must be strings, got {type(resource_name)} and {type(resource_type)} instead")
            if resource_type == "pod":
                self.client.read_namespaced_pod(namespace='default', name=resource_name)
            elif resource_type == "service":
                self.client.read_namespaced_service(namespace='default', name=resource_name)
            else:
                raise ValueError("This resource is either invalid or not implemented")
            return True
        except Exception:
            return False

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