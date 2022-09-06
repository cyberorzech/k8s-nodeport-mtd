import psutil
from loguru import logger

from mtd_sources.logger import initialize

def main():
    while True:
        ONE_SECOND = 1
        cpu_usage = psutil.cpu_percent(ONE_SECOND)
        mem_usage = psutil.virtual_memory()
        logger.success(f"{cpu_usage=}%, {mem_usage[2]=}%")

if __name__ == "__main__":
    initialize("config.yaml")
    main()