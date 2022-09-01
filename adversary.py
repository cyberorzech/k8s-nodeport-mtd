from loguru import logger
from subprocess import check_output

from mtd_sources.logger import initialize

@logger.catch
def perform_port_scan(target_ip: str):
    pass

@logger.catch
def find_legitimate_app(target_ip: str, open_ports: list):
    pass

@logger.catch
def exploit():
    pass

@logger.catch
def send_request(target_ip: str, port: str):
    pass

@logger.catch
def main():
    pass

if __name__ == "__main__":
    initialize("config.yaml")
    main()