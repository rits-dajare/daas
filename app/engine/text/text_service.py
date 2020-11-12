import re
from .katakanizer import Katakanizer


class TextService:
    def __init__(self):
        self.__katakanizer = Katakanizer()

    def katakanize(self, text, use_api=True):
        return self.__katakanizer.katakanize(text, use_api)

    def morphs(self, text):
        return self.__katakanizer.morphs(text)

    def cleaned(self, text):
        # ノイズを除去
        result = re.sub(
            r'[^0-9A-Za-z\u3041-\u3096\u30A1-\u30F6\u3005-\u3006\u3400-\u3fff\u2E80-\u2FDF\u3005-\u3007\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\U00020000-\U0002EBEFー〜 ]', '', text)
        # '笑'を意味する'w'を除去
        result = re.sub(r'^(?![a-vx-zA-Z])w+^(?![a-vx-zA-Z])', '', result)
        result = re.sub(r'w{2,}', '', result)

        return result

    def count_char_matches(self, s1, s2):
        if len(s1) != len(s2):
            return 0

        result = 0
        for i in range(len(s1)):
            if s1[i] == s2[i]:
                result += 1

        return result

    def n_gram(self, text, n=3):
        return [text[idx:idx + n] for idx in range(len(text) - n + 1)]

    def normalize(self, text):
        patterns = [
            'ヲヂガギグゲゴザジズゼゾダヂヅデドバビブヴベボパピプペポ〜',
            'オジカキクケコサシスセソタチツテトハヒフフヘホハヒフヘホー'
        ]
        for i in range(len(patterns[0])):
            text = text.replace(
                patterns[0][i],
                patterns[1][i]
            )

        # 3回以上繰り返された文字を1文字に圧縮
        text = re.sub(r'(.)\1{2,}', r'\1', text)

        return text

    def conv_vector(self, text, size=None):
        result = list(map(ord, text))

        # トリミング&パディング
        if size is not None:
            result = result[:size]
            result += [0] * (size - len(result))

        return result
