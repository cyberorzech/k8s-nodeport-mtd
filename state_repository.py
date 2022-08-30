from loguru import logger
from flask import Flask
from flask_restful import Api

#from mtd_sources.logger import initialize
from mtd_sources.state import State


if __name__ == "__main__":
    # CONFIG_FILE_PATH = "./config.yaml"
    # initialize(CONFIG_FILE_PATH)
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(State, "/state")
    app.run()
    #state_repository()