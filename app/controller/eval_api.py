from flask import Blueprint
from flask_restful import Api
from .api import API
import engine


class EvalAPI(API):
    def _args_validation(self, args):
        return 'dajare' in args

    def _processing(self, args):
        result = {
            'score': None,
        }

        result['score'] = engine.eval_engine.eval(args['dajare'])

        return result


bp = Blueprint('eval', __name__)
api = Api(bp)
api.add_resource(EvalAPI, '')
