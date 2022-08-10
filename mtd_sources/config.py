import sys
from yaml import load, FullLoader
from loguru import logger


def get_config(config_path):
    try:
        with open(config_path) as file:
            config = load(file, Loader=FullLoader)
        return config
    except Exception as e:
        logger.error(e)
        sys.exit()


def main():
    raise NotImplementedError("Use as package")


if __name__ == "__main__":
    main()
