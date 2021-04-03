import unittest

from core import config
from core import preprocessing


class TestAPI(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_reading(self):
        self.assertEqual('コンニチハ', preprocessing.reading('こんにちは'))
        self.assertEqual('フトンガフットンダ', preprocessing.reading('布団が吹っ飛んだ'))
        # with dict
        self.assertEqual('アルドゥイーノ', preprocessing.reading('Arduino'))

    def test_convert_morphs(self):
        self.assertEqual(['キョウ', 'ノ', 'テンキ'], preprocessing.convert_morphs('今日の天気'))

    def test_filtering(self):
        test_cases: list = [
            ['', '!@#$%^^&*()，。/-_=+;:'],
            ['', '🤗⭕🤓🤔🤘🦁⭐🆗🆖🈲🤐🤗🤖🤑🆙⏩'],
            ['布団が吹っ飛んだ', '布団が吹っ飛んだ'],
        ]
        for case in test_cases:
            self.assertEqual(case[0], preprocessing.filtering(case[1]))

    def test_n_gram(self):
        self.assertEqual(['あい', 'いう', 'うえ', 'えお'], preprocessing.n_gram('あいうえお', 2))
        self.assertEqual(['あいう', 'いうえ', 'うえお'], preprocessing.n_gram('あいうえお', 3))
        self.assertEqual(['あいうえ', 'いうえお'], preprocessing.n_gram('あいうえお', 4))
        self.assertEqual(['あいうえお'], preprocessing.n_gram('あいうえお', 5))

    def test_normalize(self):
        self.assertEqual('カキクケコ', preprocessing.normalize('ガギグゲゴ'))
        self.assertEqual('アイイ', preprocessing.normalize('アアアイイ'))

    def test_vectorize(self):
        text: str = 'こんにちは'
        self.assertEqual(
            [12371, 12435, 12395, 12385, 12399] + [0] * (config.TEXT_MAX_LENGTH - len(text)),
            preprocessing.vectorize(text)
        )
