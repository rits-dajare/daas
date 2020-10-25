# -*- coding: utf-8 -*-
import re


class Engine():
    def __init__(self, katakanizer):
        self.katakanizer = katakanizer
        self._setup()

    def _setup(self):
        raise Exception('サブクラスの責務')

    def exclude_noise(self, text):
        noise = re.compile(
            r'[^0-9A-Za-z\u3041-\u3096\u30A1-\u30F6\u3005-\u3006\u3400-\u3fff\u2E80-\u2FDF\u3005-\u3007\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\U00020000-\U0002EBEFー]')
        return noise.sub('', text)

    def to_reading(self, text, use_api=True):
        text = self.exclude_noise(text)
        return self.katakanizer.katakanize(text, use_api)
