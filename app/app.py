from flask import Flask
from controller import judge_api
from controller import eval_api
from controller import reading_api


def create_app() -> Flask:
    app = Flask(__name__)

    @app.after_request
    def add_header(res):
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

    import controller

    app.register_blueprint(controller.judge_api, url_prefix='/judge/')
    app.register_blueprint(controller.eval_api, url_prefix='/eval/')
    app.register_blueprint(controller.reading_api, url_prefix='/reading/')

    return app
