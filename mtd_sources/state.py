from loguru import logger
from flask_restful import Resource, reqparse
#from requests import get

class State(Resource):
    def __init__(cls) -> None:
        super().__init__()
        cls.state = None

    @logger.catch
    def get(cls):
        args = cls.__get_args()

        return dict(args), 200

    @logger.catch
    def __update(cls):
        res = get("localhost:5100")
        cls.state = res.json

    @logger.catch
    def __print(cls):
        raise NotImplementedError()


    def __get_args(cls):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("os")
        parser.add_argument("vendor")
        parser.add_argument("model")
        parser.add_argument("start_date")
        parser.add_argument("end_date")
        args = parser.parse_args()
        return args


if __name__ == "__main__":
    raise NotImplementedError("Use as class")




