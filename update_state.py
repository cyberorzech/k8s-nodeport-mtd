from time import sleep
from loguru import logger
from requests import get
from json import dump

from mtd_sources.logger import initialize
from mtd_sources.config import get_config

# INTERVAL = 10 # [s]
# APP_RECONFIGURATOR_URL = "http://localhost:5100/update"
# STATE_PATH = "./state.json"
CONFIG_PATH = "./config.yaml"

@logger.catch
def update_state(once=False):
    config = get_config(CONFIG_PATH)
    INTERVAL = config["STATE_UPDATE_INTERVAL"] # [s]
    APP_RECONFIGURATOR_URL = config["APP_RECONFIGURATOR_URL"]
    STATE_PATH = config["STATE_PATH"]
    while True:
        response = get(APP_RECONFIGURATOR_URL)
        with open(STATE_PATH, "w") as f:
            dump(response.json(), f)
        logger.success("State updated")
        if once:
            break
        sleep(INTERVAL)


if __name__ == "__main__":
    initialize("./config.yaml")
    update_state()