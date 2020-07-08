# -*- coding: utf-8 -*-

from functools import lru_cache
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


def check_health(res, alert=True):
    code = res.status_code
    try:
        assert code == requests.codes.ok
    except:
        url = 'https://notify-api.line.me/api/notify'
        header = {'Authorization': 'Bearer ' + LINE}

        try:
            # send message from LINE
            if alert:
                message = open('config/alert.txt', 'r').read()
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                message = message.replace('{timestamp}', timestamp)
                message = message.replace('{code}', str(code))
                message = message.replace('{url}', res.url)
                message = message.replace('{json}', str(res.json()))

                param = {'message': message}
                requests.post(url, headers=header, params=param)
        except:
            pass

        return False

    return True


@lru_cache(maxsize = 255)
def to_reading(dajare):
    url = 'https://api.apigw.smt.docomo.ne.jp/gooLanguageAnalysis/v1/hiragana?APIKEY={}'
    headers = {'Content-Type': 'application/json'}
    params = {'sentence': dajare, 'output_type': 'katakana'}

    for key in APIKEY:
        goo_api.set_url(url.format(key))
        res = goo_api.post(
            headers,
            json.dumps(params)
        )
        if check_health(res, False):
            return res

    return res


@lru_cache(maxsize = 255)
def find_sensitive_tags(dajare):
    url = 'https://api.apigw.smt.docomo.ne.jp/truetext/v1/sensitivecheck?APIKEY={}'
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
    params = { 'text': dajare }

    for key in APIKEY:
        jetrun_api.set_url(url.format(key))
        res = jetrun_api.post(
            headers,
            params
        )
        if check_health(res, False):
            return res

    return res

