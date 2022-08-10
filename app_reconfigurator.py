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
    patch_file_template = config["PATCH_FILE_TEMPLATE"]
    if not isinstance(services_names, list) or len(services_names) < 1:
        raise ValueError(f"Invalid services names in config (either not a list or empty list)")
    k8s = K8s()
    for name in services_names:
        k8s.check_resource_existence(name, "service")

    legit_service_name = choice(services_names)
    # zaladuj templatke
    template = load_template(patch_file_template)
    # dla kazdego servicename:
    for name in services_names:
        pass
    # przygotuj templatke
    # -f apply
    # print raport



    # pojedyncze przygotowanie
    template["spec"]["selector"] = {"app": "legit-app"}
    print("template po poprawce: ")
    print(template)
    k8s.patch_service("app-service2", template)

@logger.catch
def prepare_patch_file(template: dict, service_name: str, id: int):
    pass


@logger.catch
def load_template(template_path: str):
    with open(path.join(path.dirname(__file__), template_path)) as f:
        file_content = safe_load(f)
    if not file_content:
        raise TypeError("Template is empty or has invalid path")
    return file_content




if __name__ == "__main__":
    CONFIG_FILE_PATH = "./config.yaml"
    initialize(CONFIG_FILE_PATH)
    app_reconfigurator()
