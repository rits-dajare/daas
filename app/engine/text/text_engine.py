import os
import json
import requests
from .token import Token


class TextEngine():
    def __init__(self):
        self.__tokens = self.__read_tokens()

        self._sub_init()

    def _sub_init(self):
        pass

    def _call_api(self, url, headers, params):
        for i in range(len(self.__tokens)):
            res = requests.post(
                '%s?APIKEY=%s' % (url, self.__tokens[i].token),
                headers=headers,
                data=params,
            )

            if self.__check_health(res):
                self.__tokens[i].enable()
                return res.json()
            else:
                self.__tokens[i].disable()

        return None

    def __check_health(self, res):
        code = res.status_code
        return code == requests.codes.ok

    def __read_tokens(self, tokens_file='config/docomo_token'):
        result = []
        if not os.path.exists(tokens_file):
            print('ファイル%sが存在しません' % tokens_file)
            return result

        with open(tokens_file, 'r') as f:
            result = f.read().split('\n')
        result.remove('')
        result = list(map(Token, result))

        return result

    @property
    def token_valid(self):
        for token in self.__tokens:
            if token.is_valid:
                return True

        return False
