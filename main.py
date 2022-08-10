from kubernetes import client, config
from loguru import logger

from mtd_sources.config import get_config
from mtd_sources.logger import initialize


def setup():
    # TODO
    # stworz deployment x2
    # sprawdz czy powstaly pody
    # stworz nodeport x2
    # sprawdz czy powstaly
    # wez porty udostepnione
    # sprawdz czy aplikacja jest dostepna
    pass


def cleanup(deployments, services):
    # TODO
    # sprawdz czy takie istnieja
    # usun
    pass


def check_cluster_connection():
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


def main():
    config = get_config(CONFIG_FILE_PATH)
    print(config["SERVICES_NAMES"])


if __name__ == "__main__":
    CONFIG_FILE_PATH = "./config.yaml"
    initialize(CONFIG_FILE_PATH)
    main()
