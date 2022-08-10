from random import choice
from loguru import logger
from yaml import safe_load
from os import path

from mtd_sources.config import get_config
from mtd_sources.logger import initialize
from mtd_sources.k8s_client import K8s


@logger.catch
def app_reconfigurator():
    config = get_config(CONFIG_FILE_PATH)
    services_names = config["SERVICES_NAMES"]
    patch_file_template = config["PATH_FILE_TEMPLATE"]
    if not isinstance(services_names, list) or len(services_names) < 1:
        raise ValueError(f"Invalid services names in config (either not a list or empty list)")
    k8s = K8s()
    for name in services_names:
        k8s.check_resource_existence(name, "service")

    legit_service_name = services_names[choice(services_names)]
    # zaladuj templatke
    template = load_template(patch_file_template)
    # dla kazdego servicename:
    for name in services_names:
        pass
    # przygotuj templatke
    # -f apply
    # print raport

@logger.catch
def prepare_patch_file(template: dict, service_name: str, id: int):
    pass


@logger.catch
def load_template(template_path: str):
    with open(path.join(path.dirname(__file__), template_path)) as f:
        file_content = safe_load(f)
    return file_content




if __name__ == "__main__":
    CONFIG_FILE_PATH = "./config.yaml"
    initialize(CONFIG_FILE_PATH)
    app_reconfigurator()
