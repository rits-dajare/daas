from flask import Blueprint
from flask_restful import Api
from .api import API
import engine


class ReadingAPI(API):
    def _args_validation(self, args):
        return 'dajare' in args

    def _processing(self, args):
        result = {
            'reading': None,
        }

        result['reading'] = engine.reading_engine.execute(args['dajare'])

        return result


bp = Blueprint('reading', __name__)
api = Api(bp)
api.add_resource(ReadingAPI, '')
