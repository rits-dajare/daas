import unittest
from parameterized import parameterized

from app import config
from app.util import text_util


class TestTextUtil(unittest.TestCase):
    @parameterized.expand([
        ['こんにちは', 'コンニチハ'],
        ['Arduino', 'アルドゥイーノ'],
        ['ABCD', 'エービーシーディー'],
        ['abcd', ''],
        ['千二百三十四', 'センニヒャクサンジュウヨン'],
    ])
    def test_正_読みに変換(self, text: str, reading: str):
        self.assertEqual(reading, text_util.reading(text))

    @parameterized.expand([
        [False, '布団が吹っ飛んだ', ['フトン', 'ガ', 'フットン', 'ダ']],
        [True, '布団が吹っ飛んだ', ['フトン', 'フットン']],
    ])
    def test_正_形態素解析(self, filtering: bool, text: str, morphs: list[str]):
        self.assertEqual(morphs, text_util.convert_morphs(text, filtering))

    @parameterized.expand([
        ['!@#$%^^&*()，。/-_=+;:', ''],
        ['🤗⭕🤓🤔🤘🦁⭐🆗🆖🈲🤐🤗🤖🤑🆙⏩', ''],
        ['布団が吹っ飛んだwwwWWWｗｗｗＷＷＷ', '布団が吹っ飛んだ'],
        ['wwwwaa', 'wwwwaa'],
        ['ｈｅｌｌｏ', 'hello'],
        ['1234', '千二百三十四'],
        ['布団が吹っ飛んだ', '布団が吹っ飛んだ'],
    ])
    def test_正_前処理(self, text: str, preprocessed_text: str):
        self.assertEqual(preprocessed_text, text_util.preprocessing(text))

    @parameterized.expand([
        [2, '布団が吹っ飛んだ', ['布団', '団が', 'が吹', '吹っ', 'っ飛', '飛ん', 'んだ']],
        [3, '布団が吹っ飛んだ', ['布団が', '団が吹', 'が吹っ', '吹っ飛', 'っ飛ん', '飛んだ']],
        [4, '布団が吹っ飛んだ', ['布団が吹', '団が吹っ', 'が吹っ飛', '吹っ飛ん', 'っ飛んだ']],
        [5, '布団が吹っ飛んだ', ['布団が吹っ', '団が吹っ飛', 'が吹っ飛ん', '吹っ飛んだ']],
    ])
    def test_正_n_gram(self, n: int, text: str, n_gram: list[str]):
        self.assertEqual(n_gram, text_util.n_gram(text, n))

    @parameterized.expand([
        ['ヲヂガギグゲゴザジズゼゾダヂヅデドバビブヴベボパピプペポ〜', 'オシカキクケコサシスセソタシツテトハヒフフヘホハヒフヘホー'],
        ['アアアイイ', 'アイイ'],
        ['アアアアアア', 'ア'],
    ])
    def test_正_テキストの正規化(self, text: str, normalized_text: str):
        self.assertEqual(normalized_text, text_util.normalize(text))

    @parameterized.expand([
        ['布団が吹っ飛んだ', [24067, 22243, 12364, 21561, 12387, 39131, 12435, 12384]]
    ])
    def test_正_テキストを文字コードのベクトルに変換(self, text: str, vector: list[int]):
        vector = vector + [0] * (config.TEXT_MAX_LENGTH - len(text))
        self.assertEqual(
            vector,
            text_util.vectorize(text)
        )
