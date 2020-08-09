# -*- coding: utf-8 -*-
import re
from . import alphabet


class ReadingService():
    def __init__(self):
        from .withapi import WithAPI
        from .withoutapi import WithoutAPI
        self.conv_with_api = WithAPI()
        self.conv_without_api = WithoutAPI()

    def convert(self, text, use_api=True):
        result = ''
        api_status = False

        # '笑'を意味する'w'を削除
        noise = re.compile(r'[^a-vx-zA-VX-Z]w+')
        text = noise.sub('', text)

        if use_api:
            result, api_status = self.conv_with_api.text_to_reading(text)
        if not api_status:
            result = self.conv_without_api.text_to_reading(text)[0]

        # 読みの分からない4文字以上の英単語を削除
        words = re.findall(r'[a-zA-Z][a-z]{3,}', text)
        for w in words:
            result = result.replace(alphabet.convert_word_to_alphabet(w.lower()), '')

        return result
