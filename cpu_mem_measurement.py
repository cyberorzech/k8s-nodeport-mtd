import psutil
import sys
import signal
import pandas as pd
from loguru import logger
from time import perf_counter

from mtd_sources.logger import initialize
from mtd_sources.config import get_config


@logger.catch
def measure():
    export_path = get_config("config.yaml")["EXPORT_PATH"]
    COLUMNS = ["timestamp", "cpu_usage [%]", "mem_usage [%]"]
    results = pd.DataFrame(columns=COLUMNS)
    start_time = perf_counter()
    while True:
        ONE_SECOND = 1
        cpu_usage = psutil.cpu_percent(ONE_SECOND)
        mem_usage = psutil.virtual_memory()
        logger.success(f"{cpu_usage=}%, {mem_usage[2]=}%")

        stop_time = perf_counter()
        timestamp = stop_time - start_time
        data = pd.DataFrame(
            columns=COLUMNS, data=[[timestamp, cpu_usage, mem_usage[2]]]
        )
        results = pd.concat([results, data])
        results.reset_index()
        results.to_csv(export_path)
        logger.success("Results exported to csv")


@logger.catch
def signal_handler(sig, frame):
    logger.info("sigint detected")
    sys.exit(0)


if __name__ == "__main__":
    initialize("config.yaml")
    signal.signal(signal.SIGINT, signal_handler)
    measure()
