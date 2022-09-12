import argparse
from loguru import logger
from requests import get
from requests.exceptions import InvalidURL
from time import sleep, perf_counter

from mtd_sources.config import get_config
from mtd_sources.logger import initialize

SERVICE_NAME = "legit_app"
CONFIG_PATH = "./config.yaml"
LEGIT_APP_MESSAGE = "This is a legitimate app"


@logger.catch
def user():
    config = get_config(CONFIG_PATH)
    NODE_IP = config["MASTER_NODE_IP"]
    successful_requests = 0
    unsuccessful_requests = 0
    state_repo_url = config["STATE_REPOSITORY_URL"]
    while True:
        response = get(f"{state_repo_url}?service_name={SERVICE_NAME}")
        try:
            service_port = response.json()
            if not isinstance(service_port, int):
                raise TypeError(
                    f"Expected type of service port: int. Got {type(service_port)} instead."
                )
        except TypeError as te:
            logger.error(te)


        response = get(f"http://{NODE_IP}:{service_port}").text
        if LEGIT_APP_MESSAGE in response:
            successful_requests += 1
            logger.success(f"Successful requests: {successful_requests}")
        else:
            unsuccessful_requests += 1
            logger.warning(f"Unsuccessful requests: {unsuccessful_requests}")
        sleep(config["USER_INTERVAL"])




@logger.catch
def measure_uptime():
    config = get_config(CONFIG_PATH) 
    NODE_IP = config["MASTER_NODE_IP"]
    downtime = 0
    uptime = 0
    loop_count = 0
    state_repo_url = config["STATE_REPOSITORY_URL"]

    while(True):
        start_time = perf_counter()
        response = get(f"{state_repo_url}?service_name={SERVICE_NAME}")
        try:
            service_port = response.json()
            if not isinstance(service_port, int):
                raise TypeError(
                    f"Expected type of service port: int. Got {type(service_port)} instead."
                )
        except TypeError as te:
            logger.error(te)
        try:
            response = get(f"http://{NODE_IP}:{service_port}").text
        except InvalidURL:
            continue

        
        
        if LEGIT_APP_MESSAGE in response:
            end_time = perf_counter()
            uptime += end_time - start_time
        else:
            end_time = perf_counter()
            downtime += end_time - start_time
        loop_count += 1
        if loop_count % 300 == 0:
            logger.success(f"Uptime: {round(uptime, 2)}[s], Downtime: {round(downtime, 2)}[s]")
            loop_count = 0
        
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", default="uptime", choices=["user", "uptime"])
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()
    if args.mode == "user": user()
    else: measure_uptime()
