# -*- coding: utf-8 -*-
from functools import lru_cache

class Converter():
    def __init__(self):
        self._setup()

    @lru_cache(maxsize=255)
    def text_to_reading(self, text):
        return self._convert_reading(text)

    def _setup(self):
        raise Exception('サブクラスの責務')

    def _convert_reading(self, text):
        raise Exception('サブクラスの責務')

