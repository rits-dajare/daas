from flask import Blueprint, request
from flask_restful import Resource, Api
from .api import API
from engine.api import *

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

        result['reading'] = katakanizer.katakanize(args['dajare'])

        return result


api.add_resource(ReadingAPI, '/reading/')
