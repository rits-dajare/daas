import re


class TextService:
    def __init__(self):
        from .katakanizer import Katakanizer
        self.__katakanizer = Katakanizer()

        from .sensitive_checker import SensitiveChecker
        self.__sensitive_checker = SensitiveChecker()

    def katakanize(self, text, use_api=True):
        return self.__katakanizer.execute(text, use_api)

    def morphs(self, text):
        return self.__katakanizer.morphs(text)

    def sensitive_check(self, text):
        return self.__sensitive_checker.execute(text)

    def cleaned(self, text):
        # ノイズを除去
        result = re.sub(
            r'[^0-9A-Za-z\u3041-\u3096\u30A1-\u30F6\u3005-\u3006\u3400-\u3fff\u2E80-\u2FDF\u3005-\u3007\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\U00020000-\U0002EBEFー〜 ]', '', text)
        # '笑'を意味する'w'を除去
        result = re.sub(r'^(?![a-vx-zA-Z])w+^(?![a-vx-zA-Z])', '', result)
        result = re.sub(r'w{2,}', '', result)

        return result

    def count_char_matches(self, ch1, ch2):
        if len(ch1) != len(ch2):
            return 0

        result = 0
        for i in range(len(ch1)):
            if ch1[i] == ch2[i]:
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

    @property
    def token_valid(self):
        return self.__katakanizer.token_valid \
            and self.__sensitive_checker.token_valid
