from loguru import logger
from kubernetes import client, config


class K8s:
    def __init__(cls) -> None:
        cls.client = cls.__check_cluster_connection()

    @logger.catch
    def check_resource_existence(cls, resource_name: str, resource_type: str) -> bool:
        if not isinstance(resource_name, str) or not isinstance(resource_type, str):
            raise TypeError(
                f"Arguments must be strings, got {type(resource_name)=} and {type(resource_type)=} instead"
            )
        if resource_type == "pod":
            res = cls.client.read_namespaced_pod(
                namespace="default", name=resource_name
            )
        elif resource_type == "service":
            res = cls.client.read_namespaced_service(
                namespace="default", name=resource_name
            )
        else:
            raise ValueError("This resource is either invalid or not implemented")
        return

    @logger.catch
    def get_nodeport(cls, resource_name: str) -> int:
        if not isinstance(resource_name, str):
            raise TypeError(f"Argument must be str, got {type(resource_name)}")
        res = cls.client.read_namespaced_service(
            namespace="default", name=resource_name
        )
        logger.info(
            "This method returns only first node port (assuming only one nodeport)"
        )
        return res.spec.ports[0].node_port

    @logger.catch
    def patch_service(cls, name: str, body: dict):
        if not isinstance(name, str) or not isinstance(body, dict):
            raise TypeError(
                f"Arguments must be string and dict, got {type(name)=} and {type(body)=}"
            )
        cls.client.patch_namespaced_service(name=name, namespace="default", body=body)

    @logger.catch
    def __check_cluster_connection(cls):
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
