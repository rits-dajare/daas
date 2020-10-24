from flask import Blueprint, request
from flask_restful import Resource, Api
from .api import API
from engine.api import *

app = Blueprint('eval', __name__)
api = Api(app)


@app.after_request
def add_header(res):
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


class EvalAPI(API):
    def _args_validation(self, args):
        return 'dajare' in args

    def _processing(self, args):
        result = {
            'score': None,
        }

        result['score'] = eval_engine.eval(args['dajare'])

        return result


api.add_resource(EvalAPI, '/eval/')
