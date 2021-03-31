import re
import csv
from functools import lru_cache
import jaconv
from janome.tokenizer import Tokenizer
from .alphabet import convert_word_to_alphabet


class Katakanizer:
    def __init__(self):
        from .docomo_service import DocomoService
        self.__docomo_service = DocomoService()

        self.katakanize_patterns = self.__load_patterns()
        self.tokenizer = Tokenizer()

    @lru_cache(maxsize=255)
    def execute(self, text, use_api=True):
        # カタカナ化するパターンを元に変換
        result = self.__force_katakanize(text)

        # カタカナ化
        use_api = use_api and self.token_valid
        katakana = ''
        if use_api:
            katakana = self.__conv_with_api(result)
        if not use_api or katakana == '':
            katakana = self.__conv_without_api(result)
        result = katakana

        # 読みの分からない英単語を変換
        result = re.sub(r'[a-zA-Z][a-z]+', '', result)
        words = re.findall(r'[a-zA-Z]+', result)
        for w in words:
            result = result.replace(w, convert_word_to_alphabet(w.lower()))

        return result

    def morphs(self, text):
        result = []
        for token in self.tokenizer.tokenize(text):
            if token.reading == '*':
                result.append(jaconv.hira2kata(token.surface))
            else:
                result.append(token.reading)

        return result

    def __conv_with_api(self, text):
        return self.__docomo_service.katakanize(text)

    def __conv_without_api(self, text):
        return ''.join(self.morphs(text))

    def __force_katakanize(self, text):
        result = text

        for pattern in self.katakanize_patterns:
            result = re.sub(*pattern, result)

        return result

    def __load_patterns(self):
        result = []
        with open('conf/katakanize_patterns.csv') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row == []:
                    continue
                result.append(row)

        return result

    @property
    def token_valid(self):
        return self.__docomo_service.is_valid
