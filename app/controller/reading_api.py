from flask import Blueprint
from flask_restful import Api
from .api import API
import engine

app = Blueprint('reading', __name__)
api = Api(app)


@app.after_request
def add_header(res):
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


class ReadingAPI(API):
    def _args_validation(self, args):
        return 'dajare' in args

    def _processing(self, args):
        result = {
            'reading': None,
        }

        result['reading'] = engine.katakanizer.katakanize(args['dajare'])

        return result


api.add_resource(ReadingAPI, '/reading/')
