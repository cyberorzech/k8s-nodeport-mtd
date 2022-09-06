import os
from loguru import logger
from subprocess import check_output
from requests import get
from time import sleep

from mtd_sources.logger import initialize
from mtd_sources.config import get_config
from mtd_sources.probability import draw
from update_state import update_state

config = get_config("./config.yaml")
TARGET_IP = config["MASTER_NODE_IP"]
LOWEST_NODE_PORT = config["LOWEST_NODE_PORT"]
HIGHEST_NODE_PORT = config["HIGHEST_NODE_PORT"]


@logger.catch
def perform_port_scan(target_ip: str, detection_probability=0.0) -> list:
    """
    Function that performs nmap scan and open ports extraction. If scan is detected, it is performed anyway.
    """
    command = f"nmap -p {LOWEST_NODE_PORT}-{HIGHEST_NODE_PORT} {target_ip} "
    command += "| grep open | awk '{print $1}' | grep -Eo '[0-9]*'"
    try:
        if os.name != "posix":
            raise RuntimeError(
                f"Port scan works only on posix os. Got {os.name} instead."
            )
    except RuntimeError as re:
        logger.error(re)
        exit(1)
    bash_output = check_output(command, shell=True)
    bash_output_str = bash_output.decode("utf-8")
    open_ports = bash_output_str.split("\n")[
        :-1
    ]  # last element is dropped because it is empty (contains no port number)
    open_ports = [int(el) for el in open_ports]
    if draw(probability=detection_probability):
        update_state(once=True)
    return open_ports


@logger.catch
def find_legitimate_app(target_ip: str, open_ports: list):
    legitimate_port = None
    for port in open_ports:
        response = send_request(target_ip, port)
        if "legitimate" in response:
            legitimate_port = port
            return True, legitimate_port
    return False, None


@logger.catch
def exploit():
    while True:
        exploit_time = config["EXPLOIT_TIME"]
        sleep(exploit_time)
        probability_of_success = get_config("config.yaml")["P1"]
        if draw(probability=probability_of_success):
            break


@logger.catch
def send_request(target_ip: str, port: str):
    """
    Function sends GET method to K8s based service and parse response
    """
    url = f"http://{target_ip}:{port}"
    res = get(url).text
    return res


@logger.catch
def scenario_1():
    successful_exploits = 0
    unsuccessful_exploits = 0
    while True:
        logger.info(f"Target IP is set to {TARGET_IP}")
        open_ports = perform_port_scan(TARGET_IP)
        logger.info(f"Open ports are: {open_ports}")
        # For every port: exploit and check if the service is legitimate
        for port in open_ports:
            exploit()
            app_response = send_request(TARGET_IP, port)
            if not "legitimate" in app_response:
                unsuccessful_exploits += 1
                logger.info(f"{unsuccessful_exploits=}")
                continue
            successful_exploits += 1
            logger.success(f"Successfully exploited app at {TARGET_IP}:{port}")
            logger.success(f"{successful_exploits=}")


@logger.catch
def scenario_2():
    successful_exploits = 0
    unsuccessful_exploits = 0
    while True:
        logger.info(f"Target IP is set to {TARGET_IP}")
        open_ports = perform_port_scan(TARGET_IP)
        logger.info(f"Open ports are: {open_ports}")
        legit_app_found, legitimate_port = find_legitimate_app(TARGET_IP, open_ports)
        if legit_app_found: 
            logger.success(f"Legitimate app found at {legitimate_port}")
            successful_exploits += 1
        else: unsuccessful_exploits += 1
        logger.info(f"{successful_exploits=}, {unsuccessful_exploits=}")
        sleep(1)


def main():
    scenario_2()


if __name__ == "__main__":
    initialize("config.yaml")
    main()
