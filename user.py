from loguru import logger
from requests import get
from time import sleep

from mtd_sources.config import get_config
from mtd_sources.logger import initialize

SERVICE_NAME = "legit_app"
CONFIG_PATH = "./config.yaml"
LEGIT_APP_MESSAGE = "This is a legitimate app"


@logger.catch
def user():
    successful_requests = 0
    unsuccessful_requests = 0
    config = get_config(CONFIG_PATH)
    state_repo_url = config["STATE_REPOSITORY_URL"]
    while True:
        response = get(f"{state_repo_url}?service_name={SERVICE_NAME}")
        try:
            service_port = response.json()
            if not isinstance(service_port, int): raise TypeError(f"Expected type of service port: int. Got {type(service_port)} instead.")
        except TypeError as te:
            logger.error(te)

        NODE_IP = config["MASTER_NODE_IP"]
        response = get(f"http://{NODE_IP}:{service_port}").text
        if LEGIT_APP_MESSAGE in response:
            successful_requests += 1
            logger.success(f"Successful requests: {successful_requests}")
        else:
            unsuccessful_requests += 1
            logger.warning(f"Unsuccessful requests: {unsuccessful_requests}")
        sleep(config["USER_INTERVAL"])

if __name__ == "__main__":
    user()