# -*- coding: utf-8 -*-
import os
from .tokens import Tokens


class DocomoTokens(Tokens):
    def _read_tokens(self):
        result = []
        is_valid = False

        token_file = './config/docomo_token'
        if not os.path.isfile(token_file):
            print('アクセストークンを指定してください')
            return result, is_valid

        with open(token_file, 'r') as f:
            result = f.read().split('\n')
        result.remove('')

        is_valid = result != []
        return result, is_valid
