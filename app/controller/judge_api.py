from flask import Blueprint, request
from flask_restful import Resource, Api
from .api import API
from engine.api import *

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

        result['is_dajare'] = judge_engine.is_dajare(args['dajare'])
        result['sensitive_tags'] = sensitive_checker.check(args['dajare'])
        result['include_sensitive'] = result['sensitive_tags'] != []

        return result


api.add_resource(JudgeAPI, '/judge/')
