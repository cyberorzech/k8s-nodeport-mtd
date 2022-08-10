from random import choice
from loguru import logger

from mtd_sources.config import get_config
from mtd_sources.logger import initialize
from mtd_sources.k8s_client import K8s


@logger.catch
def app_reconfigurator():
    config = get_config(CONFIG_FILE_PATH)
    services_names = config["SERVICES_NAMES"]
    if not isinstance(services_names, list) or len(services_names) < 1:
        raise ValueError(f"Invalid services names in config (either not a list or empty list)")
    k8s = K8s()
    for name in services_names:
        k8s.check_resource_existence(name, "service")

    legit_service_name = services_names[choice(services_names)]
    



if __name__ == "__main__":
    CONFIG_FILE_PATH = "./config.yaml"
    initialize(CONFIG_FILE_PATH)
    app_reconfigurator()
