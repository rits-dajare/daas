# -*- coding: utf-8 -*-
import re
import jaconv
from functools import lru_cache


class Converter():
    def __init__(self):
        self._setup()

    @lru_cache(maxsize=255)
    def text_to_reading(self, text):
        # rutern: (reading, status)
        #   - reading: textの読み（カタカナ）
        #   - status: カタカナ変換に成功したか（boolean）
        result = list(self._convert_reading(text))
        result[0] = self.__extract_katakana(result[0])

        return result

    def _setup(self):
        raise Exception('サブクラスの責務')

    def _convert_reading(self, text):
        raise Exception('サブクラスの責務')

    def __extract_katakana(self, text):
        return ''.join(re.findall('[ァ-ヴー]+', text))
