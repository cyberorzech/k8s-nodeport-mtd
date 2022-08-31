import argparse
from scapy.all import *
from scapy.layers.http import HTTPRequest
from colorama import init, Fore
from loguru import logger

from mtd_sources.logger import initialize
from mtd_sources.config import get_config


init()
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET


class Sniffer:
    @logger.catch
    def __init__(cls) -> None:
        cls.__get_args()
        initialize("./config.yaml")

    @logger.catch
    def run(cls, iface=None):
        logger.success("Sniffing started")
        sniff(prn=cls.process_packets, iface=iface, store=False)

    @logger.catch
    def process_packets(cls, packet):
        if "ICMP" in packet.summary():
            logger.success("mam icmp!")


    @logger.catch
    def __get_args(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--iface")
        parser.add_argument("--show-raw", dest="show_raw", action="store_true")
        args = parser.parse_args()
        iface = args.iface
        show_raw = args.show_raw
        args = parser.parse_args()



if __name__ == "__main__":
    sniffer = Sniffer()
    sniffer.run()