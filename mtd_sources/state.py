from loguru import logger
from flask_restful import Resource, reqparse

class State(Resource):
    def __init__(cls) -> None:
        super().__init__()

#     @logger.catch
#     def get(cls):
#         args = cls.__get_args()
#         return {"ok": 2}, 200

#     @logger.catch
#     def __update(cls):
#         raise NotImplementedError()

#     @logger.catch
#     def __print(cls):
#         raise NotImplementedError()

#     def __get_args(cls):
#         parser = reqparse.RequestParser()
#         parser.add_argument("report")
#         args = parser.parse_args()
#         return args


# if __name__ == "__main__":
#     raise NotImplementedError("Use as class")




    def get(cls):
        try:
            args = cls.__get_args()

            # logger.success(
            #     f"Performed search for {args.id=}, {args.os=}, {args.vendor=}, {args.model=}, {args.start_date=}, {args.end_date=} in {round(end_time - start_time, 3)} seconds"
            # )
            return {}, 200
        except ValueError as ve:
            logger.error(ve)
            return str(ve), 400
        except Exception as e:
            logger.error(e)
            return str(e), 401





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
