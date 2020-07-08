# -*- coding: utf-8 -*-

import json
import requests
import http_request


# read API keys
try:
    APIKEY = open('config/docomo_token').read().split('\n')
    if '' in APIKEY:
        APIKEY.remove('')
    LINE = open('config/line_token').read().strip()
except:
    print('\033[31mError\033[0m: Configuration file does not exist')
    print('Please set config files under config/')
    exit(0)

goo_api = http_request.HTTP()
jetrun_api = http_request.HTTP()


def to_reading(dajare):
    url = 'https://api.apigw.smt.docomo.ne.jp/gooLanguageAnalysis/v1/hiragana?APIKEY={}'
    headers = { 'Content-Type': 'application/json' }
    params = {'sentence': dajare, 'output_type': 'katakana'}

    for key in APIKEY:
        goo_api.set_url(url.format(key))
        res = goo_api.post(
            headers,
            json.dumps(params)
        )

        return res


print(to_reading('布団が吹っ飛んだ').json())
