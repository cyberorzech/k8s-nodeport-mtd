from sys import exit, stdout, stderr
from loguru import logger
from datetime import date

from mtd_sources.config import get_config


def initialize(config: str):
    try:
        SETTINGS = get_config(config)
        log_filename = SETTINGS["LOG_FILE"]
        if log_filename == "auto":
            today = date.today()
            log_filename = f"logs/{today.year}-{today.month}-{today.day}.log"
        logger.remove()
        logger.add(stdout, level=SETTINGS["LOG_LVL"])
        logger.add(
            log_filename,
            level=SETTINGS["LOG_LVL"],
            colorize=True,
            retention=SETTINGS["LOG_RETENTION"],
        )
    except KeyError as key_err:
        logger.remove()
        logger.add(stderr)
        logger.critical(f"Key missing in settings file: {str(key_err)}")
        exit(1)
    except Exception as e:
        print(str(e))
        exit(1)
    finally:
        logger.debug("Logger has been initialized")


if __name__ == "__main__":
    raise NotImplementedError("Use initialize function")