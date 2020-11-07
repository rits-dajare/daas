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

    def __read_tokens(self, tokens_env='DOCOMO_TOKENS'):
        result = []
        if tokens_env not in os.environ:
            print('%s環境変数が存在しません' % tokens_env)
            return result

        tokens = os.environ['DOCOMO_TOKENS'].split(' ')
        result = list(map(Token, tokens))

        return result

    @property
    def token_valid(self):
        for token in self.__tokens:
            if token.is_valid:
                return True

        return False
