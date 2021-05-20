import unittest

from core import config
from core.util import text_util


class TestTextUtil(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_reading(self):
        self.assertEqual('コンニチハ', text_util.reading('こんにちは'))
        self.assertEqual('フトンガフットンダ', text_util.reading('布団が吹っ飛んだ'))
        # with dict
        self.assertEqual('アルドゥイーノ', text_util.reading('Arduino'))
        # alphabet
        self.assertEqual('エービーシーディー', text_util.reading('ABCD'))
        self.assertEqual('', text_util.reading('abcd'))

    def test_convert_morphs(self):
        self.assertEqual(['キョウ', 'ノ', 'テンキ'], text_util.convert_morphs('今日の天気'))

    def test_filtering(self):
        test_cases: list = [
            ['', '!@#$%^^&*()，。/-_=+;:'],
            ['', '🤗⭕🤓🤔🤘🦁⭐🆗🆖🈲🤐🤗🤖🤑🆙⏩'],
            ['布団が吹っ飛んだ', '布団が吹っ飛んだ'],
        ]
        for case in test_cases:
            self.assertEqual(case[0], text_util.filtering(case[1]))

    def test_n_gram(self):
        self.assertEqual(['あい', 'いう', 'うえ', 'えお'], text_util.n_gram('あいうえお', 2))
        self.assertEqual(['あいう', 'いうえ', 'うえお'], text_util.n_gram('あいうえお', 3))
        self.assertEqual(['あいうえ', 'いうえお'], text_util.n_gram('あいうえお', 4))
        self.assertEqual(['あいうえお'], text_util.n_gram('あいうえお', 5))

    def test_normalize(self):
        self.assertEqual('カキクケコ', text_util.normalize('ガギグゲゴ'))
        self.assertEqual('アイイ', text_util.normalize('アアアイイ'))

    def test_vectorize(self):
        text: str = 'こんにちは'
        self.assertEqual(
            [12371, 12435, 12395, 12385, 12399] + [0] * (config.TEXT_MAX_LENGTH - len(text)),
            text_util.vectorize(text)
        )
