import os
import re
import json
import requests


class DocomoService:
    def __init__(self):
        self.__is_valid = True
        self.__tokens = self.__read_tokens()

    def katakanize(self, text):
        body = self.__call_api(
            'https://api.apigw.smt.docomo.ne.jp/gooLanguageAnalysis/v1/hiragana',
            {'Content-Type': 'application/json'},
            json.dumps({'sentence': text, 'output_type': 'katakana'}),
        )

        if body is None:
            return ''
        if 'converted' not in body:
            return ''

        return body['converted'].replace(' ', '')

    def sensitive_check(self, text):
        body = self.__call_api(
            'https://api.apigw.smt.docomo.ne.jp/truetext/v1/sensitivecheck',
            {'Content-Type': 'application/x-www-form-urlencoded'},
            {'text': text},
        )

        result = []
        if body is None:
            return result
        if 'quotients' not in body:
            return result

        quotients = body['quotients']
        if not isinstance(quotients, list):
            quotients = [quotients]

        quot_names = map(lambda quot: quot['cluster_name'], quotients)
        for name in quot_names:
            # name: '項目:項目' or '項目・項目'
            result.extend(re.split(r'[:・]', name))
        result = list(set(result))
        result.sort()

        return result

    def __call_api(self, url, headers, params):
        for token in self.__tokens:
            res = requests.post(
                '%s?APIKEY=%s' % (url, token),
                headers=headers,
                data=params,
            )

            if self.__check_health(res):
                self.enable()
                return res.json()

        self.disable()
        return None

    def __check_health(self, res):
        return res.status_code == 200

    def __read_tokens(self, tokens_env='DOCOMO_TOKENS'):
        if tokens_env not in os.environ:
            print('%s環境変数が存在しません' % tokens_env)
            self.disable()
            return []

        return os.environ['DOCOMO_TOKENS'].split(' ')

    def enable(self):
        self.__is_valid = True

    def disable(self):
        self.__is_valid = False

    @property
    def is_valid(self):
        return self.__is_valid
