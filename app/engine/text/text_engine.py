import requests
import json
from .tokens.docomo import DocomoTokens


class TextEngine():
    def __init__(self):
        docomo_token = DocomoTokens()
        self.__tokens = docomo_token.tokens
        self.__token_valid = docomo_token.is_valid

        # call sub class's constructor
        self._sub_init()

    def _sub_init(self):
        pass

    def _call_api(self, url, headers, params):
        for token in self.__tokens:
            res = requests.post(
                '%s?APIKEY=%s' % (url, token),
                headers=headers,
                data=params,
            )

            if self.__check_health(res):
                self.__token_valid = True
                return res.json()

        self.__token_valid = False
        return None

    def __check_health(self, res):
        code = res.status_code
        if code == requests.codes.ok:
            return True
        else:
            return False

    @property
    def token_valid(self):
        return self.__token_valid
