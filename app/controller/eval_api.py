from flask import Blueprint
from flask_restful import Api
from .api import API
import engine

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

        result['score'] = engine.eval_engine.eval(args['dajare'])

        return result


api.add_resource(EvalAPI, '/eval/')
