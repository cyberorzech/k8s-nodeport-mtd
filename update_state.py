from time import sleep
from loguru import logger
from requests import get
from json import dump

from mtd_sources.logger import initialize

INTERVAL = 10 # [s]
APP_RECONFIGURATOR_URL = "http://localhost:5100/update"
STATE_PATH = "./state.json"

@logger.catch
def update_state():
    while True:
        response = get(APP_RECONFIGURATOR_URL)
        with open(STATE_PATH, "w") as f:
            dump(response.json(), f)
        logger.success("State updated")
        sleep(INTERVAL)

if __name__ == "__main__":
    initialize("./config.yaml")
    update_state()