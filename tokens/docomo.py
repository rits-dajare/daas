# -*- coding: utf-8 -*-
import os
from tokens.tokens import Tokens


class DocomoTokens(Tokens):
    def _read_tokens(self):
        result = []

        token_file = './config/docomo_token'
        if not os.path.isfile(token_file):
            print('アクセストークンを指定してください')
            return result

        with open(token_file, 'r') as f:
            result = f.read().split('\n')
        result.remove('')

        return result
