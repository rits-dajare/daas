# -*- coding: utf-8 -*-


class Tokens:
    def __init__(self):
        self.__tokens, self.__is_valid = self._read_tokens()

    def _read_tokens(self):
        raise Exception('サブクラスの責務')

    @property
    def tokens(self):
        return self.__tokens

    @property
    def is_valid(self):
        return self.__is_valid
