# -*- coding: utf-8 -*-
import os
import requests
import datetime
import json
from reading.converter import Converter


class WithAPI(Converter):
    def _setup(self):
        self.docomo_keys = []
        self.line_keys = []
        self.__load_apikeys()

    def _convert_reading(self, text):
        return self.__call_api(text)

    def __load_apikeys(self):
        docomo_token_file = './config/docomo_token'
        line_token_file = './config/line_token'

        if not os.path.isfile(docomo_token_file):
            raise Exception('docomo apiのアクセストークンを指定してください')
        if not os.path.isfile(line_token_file):
            raise Exception('LINE apiのアクセストークンを指定してください')

        # それぞれAPIキーをリストに格納
        with open(docomo_token_file, 'r') as f:
            self.docomo_keys.extend(f.read().split('\n'))
        with open(line_token_file, 'r') as f:
            self.line_keys.extend(f.read().split('\n'))
        self.docomo_keys.remove('')
        self.line_keys.remove('')

    def __call_api(self, text):
        url = 'https://api.apigw.smt.docomo.ne.jp/gooLanguageAnalysis/v1/hiragana?APIKEY={}'
        headers = {'Content-Type': 'application/json'}
        params = {'sentence': text, 'output_type': 'katakana'}

        for key in self.docomo_keys:
            # API呼び出し
            res = requests.post(
                url.format(key),
                headers=headers,
                data=json.dumps(params)
            )

            # レスポンスが正常な場合
            if self.__check_health(res):
                return res.json()['converted'].replace(' ', ''), True

        return '', False

    def __check_health(self, res):
        code = res.status_code
        if code == requests.codes.ok:
            return True
        else:
            return False
