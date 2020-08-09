# -*- coding: utf-8 -*-
import os
import requests
import json
from .converter import Converter
from ..tokens.docomo import DocomoTokens


class WithAPI(Converter):
    def _setup(self):
        # set docomo api access token
        tokens = DocomoTokens()
        self.tokens = tokens.get_tokens()

    def _convert_reading(self, text):
        return self.__call_api(text)

    def __call_api(self, text):
        url = 'https://api.apigw.smt.docomo.ne.jp/gooLanguageAnalysis/v1/hiragana?APIKEY={}'
        headers = {'Content-Type': 'application/json'}
        params = {'sentence': text, 'output_type': 'katakana'}

        for token in self.tokens:
            # API呼び出し
            res = requests.post(
                url.format(token),
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
