from flask import Blueprint
from flask_restful import Api
from .api import API
import engine

app = Blueprint('judge', __name__)
api = Api(app)


@app.after_request
def add_header(res):
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


class JudgeAPI(API):
    def _args_validation(self, args):
        return 'dajare' in args

    def _processing(self, args):
        result = {
            'is_dajare': None,
            'include_sensitive': None,
            'sensitive_tags': None,
        }

        result['is_dajare'] = engine.judge_engine.is_dajare(args['dajare'])
        result['sensitive_tags'] = engine.sensitive_checker.check(
            args['dajare'])
        result['include_sensitive'] = result['sensitive_tags'] != []

        return result


api.add_resource(JudgeAPI, '/judge/')
