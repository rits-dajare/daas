import os
from flask import Flask

from . import judge_api
from . import eval_api
from . import reading_api


def create_app(test_config=None) -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.after_request
    def add_header(res):
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

    @app.route('/')
    def hello():
        return 'Welcome to Dajare as a Service'

    app.register_blueprint(judge_api.bp, url_prefix='/judge/')
    app.register_blueprint(eval_api.bp, url_prefix='/eval/')
    app.register_blueprint(reading_api.bp, url_prefix='/reading/')

    app.add_url_rule('/', endpoint='index')

    return app
