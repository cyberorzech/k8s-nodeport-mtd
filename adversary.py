import os
from loguru import logger
from subprocess import check_output
from requests import get


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
    pass

@logger.catch
def send_request(target_ip: str, port: str):
    """
    Function sends GET method to K8s based service and parse response
    """
    url = f"http://{target_ip}:{port}"
    res = get(url).text
    return res

@logger.catch
def main():
    TARGET_IP = "10.2.255.1"
    open_ports = perform_port_scan(TARGET_IP)
    legitimate_app = find_legitimate_app(TARGET_IP, open_ports)
    print(legitimate_app)


if __name__ == "__main__":
    initialize("config.yaml")
    main()