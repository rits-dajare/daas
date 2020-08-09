# -*- coding: utf-8 -*-
import re
import csv
from engine import alphabet


class Engine():
    def __init__(self, reading_converter):
        self.reading_converter = reading_converter
        self._setup()

    def _setup(self):
        raise Exception('サブクラスの責務')

    def exclude_noise(self, text):
        noise = re.compile(
            r'[^0-9A-Za-z\u3041-\u3096\u30A1-\u30F6\u3005-\u3006\u3400-\u3fff\u2E80-\u2FDF\u3005-\u3007\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\U00020000-\U0002EBEFー]')
        return noise.sub('', text)

    def to_reading(self, text, use_api=True):
        result = self.exclude_noise(text)

        # '笑'を意味する'w'を削除
        noise = re.compile(r'[^a-vx-zA-VX-Z]w+')
        result = noise.sub('', result)

        result = self.reading_converter.convert(result, use_api)

        # 読みの分からない4文字以上の英単語を削除
        words = re.findall(r'[a-zA-Z][a-z]{3,}', text)
        for w in words:
            result = result.replace(alphabet.convert_word_to_alphabet(w.lower()), '')

        return result
