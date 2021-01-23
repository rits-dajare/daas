from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    @app.after_request
    def add_header(res):
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

    import webapi

    app.register_blueprint(webapi.judge_api, url_prefix='/judge/')
    app.register_blueprint(webapi.eval_api, url_prefix='/eval/')
    app.register_blueprint(webapi.reading_api, url_prefix='/reading/')

    return app
