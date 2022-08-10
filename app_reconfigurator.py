from loguru import logger

from mtd_sources.config import get_config
from mtd_sources.logger import initialize
from mtd_sources.k8s_functions import *


@logger.catch
def app_reconfigurator():
    config = get_config(CONFIG_FILE_PATH)
    selectors = config["APP_SELECTORS"]
    services_names = config["SERVICES_NAMES"]
    


if __name__ == "__main__":
    CONFIG_FILE_PATH = "./config.yaml"
    initialize(CONFIG_FILE_PATH)
    app_reconfigurator()
