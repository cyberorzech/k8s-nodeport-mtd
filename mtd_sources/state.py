from loguru import logger
from flask_restful import Resource, reqparse
from json import load

from mtd_sources.config import get_config

CONFIG_PATH = "./config.yaml"

class State(Resource):
    def __init__(cls) -> None:
        super().__init__()
        cls.state = None

    @logger.catch
    def get(cls):
        args = cls.__get_args()
        STATE_PATH = get_config(CONFIG_PATH)["STATE_PATH"]
        with open(STATE_PATH) as f:
            state = load(f)
        try:
            service_port = state[f"{args.service_name}_port"]
        except KeyError:
            logger.warning(f"Unknown service {args.service_name}")
            return None, 204
        return service_port, 200

    def __get_args(cls):
        parser = reqparse.RequestParser()
        parser.add_argument("service_name")
        args = parser.parse_args()
        return args


if __name__ == "__main__":
    raise NotImplementedError("Use as class")
