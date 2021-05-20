import os
from flask import Flask

from . import judge_controller
from . import eval_controller
from . import reading_controller


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

    # traling slash
    app.url_map.strict_slashes = False

    @app.after_request
    def add_header(res):
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

    @app.route('/')
    def hello():
        return 'Hello, World!'

    app.register_blueprint(judge_controller.bp, url_prefix='/judge')
    app.register_blueprint(eval_controller.bp, url_prefix='/eval')
    app.register_blueprint(reading_controller.bp, url_prefix='/reading')

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule('/', endpoint='index')

    return app
