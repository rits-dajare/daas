# -*- coding: utf-8 -*-


class Tokens:
    def __init__(self):
        self.tokens = self._read_tokens()

    def get_tokens(self):
        return self.tokens

    def _read_tokens(self):
        raise Exception('サブクラスの責務')
