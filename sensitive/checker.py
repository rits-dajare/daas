# -*- coding: utf-8 -*-
import os
import requests
import json
import csv
import re
from tokens.docomo import DocomoTokens


class SensitiveChecker():
    def __init__(self):
        # set docomo api access token
        tokens = DocomoTokens()
        self.tokens = tokens.get_tokens()

        # load force tagging pattern
        self.force_sensitive_pattern = []
        self.__load_tagging_pattern()

    def find_tags(self, text):
        result = self.__call_api(text)
        result.extend(self.__force_tagging(text))
        result = list(set(result))
        result.sort()

        return result

    def __force_tagging(self, text):
        result = []
        for pattern in self.force_sensitive_pattern:
            if re.search(pattern[0], text) is None:
                continue
            result.append(pattern[1])

        return result

    def __load_tagging_pattern(self):
        with open('config/force_sensitive_pattern.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if row == []:
                    continue
                self.force_sensitive_pattern.append(row)

    def __call_api(self, text):
        url = 'https://api.apigw.smt.docomo.ne.jp/truetext/v1/sensitivecheck?APIKEY={}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {'text': text}

        for token in self.tokens:
            # API呼び出し
            res = requests.post(
                url.format(token),
                headers=headers,
                data=params
            )

            # レスポンスが正常な場合
            if self.__check_health(res):
                return self.__exctract_tags_from_res(res)

        return []

    def __exctract_tags_from_res(self, res):
        result = []

        body = res.json()
        if 'quotients' not in body:
            return result

        for word_tags in body['quotients']:
            for tag in word_tags['cluster_name'].split('・'):
                if ':' in tag:
                    continue
                result.append(tag)

        return result

    def __check_health(self, res):
        code = res.status_code
        if code == requests.codes.ok:
            return True
        else:
            return False
