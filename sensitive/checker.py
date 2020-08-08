# -*- coding: utf-8 -*-
import os
import requests
import json
import csv
import re


class SensitiveChecker():
    def __init__(self):
        # load api keys
        self.docomo_keys = []
        self.line_keys = []
        self.__load_apikeys()

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
        url = 'https://api.apigw.smt.docomo.ne.jp/truetext/v1/sensitivecheck?APIKEY={}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {'text': text}

        for key in self.docomo_keys:
            # API呼び出し
            res = requests.post(
                url.format(key),
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
