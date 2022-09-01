import os
from loguru import logger
from subprocess import check_output
from requests import get
from time import sleep

from mtd_sources.logger import initialize

@logger.catch
def perform_port_scan(target_ip: str) -> list:
    command = f"nmap -p 30000-32999 {target_ip} "
    command += "| grep open | awk '{print $1}' | grep -Eo '[0-9]*'"
    try:
        if os.name != "posix":
            raise RuntimeError(f"Port scan works only on posix os. Got {os.name} instead.")
    except RuntimeError as re:
        logger.error(re)
        exit(1)
    bash_output = check_output(command, shell=True)
    bash_output_str = bash_output.decode("utf-8")
    open_ports = bash_output_str.split("\n")[:-1] # last element is dropped because it is empty (contains no port number)
    open_ports = [int(el) for el in open_ports]
    return open_ports


@logger.catch
def find_legitimate_app(target_ip: str, open_ports: list):
    legitimate_port = None
    for port in open_ports:
        response = send_request(target_ip, port)
        if "legitimate" in response:
            legitimate_port = port
            break
    return legitimate_port

@logger.catch
def exploit():
    INTERVAL = 10
    sleep(INTERVAL)

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
        TARGET_IP = "10.2.255.1"
        logger.info(f"Target IP is set to {TARGET_IP}")
        open_ports = perform_port_scan(TARGET_IP)
        logger.info(f"Open ports are: {open_ports}")
        legitimate_port = find_legitimate_app(TARGET_IP, open_ports)
        logger.info(f"Legitimate app found at {legitimate_port}")
        exploit()
        app_response = send_request(TARGET_IP, legitimate_port)
        if not "legitimate" in app_response:
            unsuccessful_exploits += 1
            logger.info(f"{unsuccessful_exploits=}")
            continue
        successful_exploits += 1
        logger.success(f"Successfully exploited app at {TARGET_IP}:{legitimate_port}")
        logger.success(f"{successful_exploits=}")

@logger.catch
def scenario_2():
    successful_exploits = 0
    unsuccessful_exploits = 0
    while True:
        TARGET_IP = "10.2.255.1"
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

def main():
    scenario_2()


if __name__ == "__main__":
    initialize("config.yaml")
    main()