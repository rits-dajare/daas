import re
import csv
import json
import jaconv
from janome.tokenizer import Tokenizer
from functools import lru_cache
from . import alphabet
from ..text_engine import TextEngine


class Katakanizer(TextEngine):
    def _sub_init(self):
        self.katakanize_patterns = self.__load_patterns()
        self.tokenizer = Tokenizer()

    @lru_cache(maxsize=255)
    def katakanize(self, text, use_api=True):
        result = text

        # カタカナ化するパターンを元に変換
        result = self.__force_katakanize(result)

        # '笑'を意味する'w'を除去
        noise = re.compile(r'(?![a-vx-zA-VX-Z])w+')
        result = noise.sub('', result)

        # カタカナ化
        if use_api and self.token_valid:
            result = self.__conv_with_api(result)
        else:
            result = self.__conv_without_api(result)

        # 読みの分からない英単語を除去
        words = re.findall(r'[a-zA-Z][a-z]{3,}', text)
        for w in words:
            result = result.replace(
                alphabet.convert_word_to_alphabet(w.lower()), '')

        return result

    def __conv_with_api(self, text):
        body = self._call_api(
            'https://api.apigw.smt.docomo.ne.jp/gooLanguageAnalysis/v1/hiragana',
            {'Content-Type': 'application/json'},
            json.dumps({'sentence': text, 'output_type': 'katakana'}),
        )

        if body is None:
            return ''
        if 'converted' not in body:
            return ''

        return body['converted'].replace(' ', '')

    def __conv_without_api(self, text):
        result = ''

        for token in self.tokenizer.tokenize(text):
            if token.reading == '*':
                # token with unknown word's reading
                result += jaconv.hira2kata(token.surface)
            else:
                # token with known word's reading
                result += token.reading

        return result

    def __force_katakanize(self, text):
        result = text

        for pattern in self.katakanize_patterns:
            result = re.sub(*pattern, result)

        return result

    def __load_patterns(self):
        result = []
        with open('config/katakanize_patterns.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if row == []:
                    continue
                result.append(row)

        return result