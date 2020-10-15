#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, abort, make_response, request
from engine.judge_engine import JudgeEngine
from engine.eval_engine import EvalEngine
from text.reading.reading_service import ReadingService
from text.sensitive.checker import SensitiveChecker

app = Flask(__name__)

# dajare engine
reading_converter = ReadingService()
judge_engine = JudgeEngine(reading_converter)
eval_engine = EvalEngine(reading_converter)

sensitive_checker = SensitiveChecker()


@app.route('/dajare/judge/', methods=['GET'])
def dajare_judge():
    '''
    uri：
        /dajare/judge
    method：
        GET
    headers：
        'Content-Type':'application/json'
    query：
        dajare: String,
    response：
        {
            is_dajare: Boolean,
            include_sensitive: Boolean,
            sensitive_tags: [String]
            status: String,
        }
    '''

    # received query params
    params = dict(request.args)

    response = {
        'is_dajare': False,
        'include_sensitive': False,
        'sensitive_tags': [],
        'status': 'OK',
    }

    # whether params could be received
    if 'dajare' not in params:
        response['status'] = 'NG'
        return make_response(jsonify(response), 400)

    # judge
    if judge_engine.is_dajare(params['dajare']):
        response['is_dajare'] = True

    # sensitive check
    response['sensitive_tags'] = \
        sensitive_checker.find_tags(params['dajare'])
    if response['sensitive_tags'] != []:
        response['include_sensitive'] = True

    return make_response(jsonify(response), 200)


@app.route('/dajare/eval/', methods=['GET'])
def dajare_evaluate():
    '''
    uri：
        /dajare/eval
    method：
        GET
    headers：
        'Content-Type':'application/json'
    query：
        dajare: String,
    response：
        {
            score: Number,
            status: String,
        }
    '''

    # received query params
    params = dict(request.args)

    response = {
        'score': 0,
        'status': 'OK',
    }

    # whether params could be received
    if 'dajare' not in params:
        response['status'] = 'NG'
        return make_response(jsonify(response), 400)

    # eval
    response['score'] = eval_engine.eval(params['dajare'])

    return make_response(jsonify(response), 200)


@app.route('/dajare/reading/', methods=['GET'])
def dajare_reading():
    '''
    uri：
        /dajare/reading
    method：
        GET
    headers：
        'Content-Type':'application/json'
    query：
        dajare: String,
    response：
        {
            reading: String,
            status: String,
        }
    '''

    # received query params
    params = dict(request.args)

    response = {
        'reading': '',
        'status': 'OK',
    }

    # whether params could be received
    if 'dajare' not in params:
        response['status'] = 'NG'
        return make_response(jsonify(response), 400)

    # convert to reading
    response['reading'] = reading_converter.convert(params['dajare'])

    return make_response(jsonify(response), 200)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    context = (
        '/etc/letsencrypt/live/conoha.abelab.dev/fullchain.pem',
        '/etc/letsencrypt/live/conoha.abelab.dev/privkey.pem'
    )
    app.run(host='0.0.0.0', port=8080, threaded=True, ssl_context=context)
