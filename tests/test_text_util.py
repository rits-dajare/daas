import unittest

from core import config
from core.util import text_util


class TestTextUtil(unittest.TestCase):
    def test_正_読みに変換(self):
        self.assertEqual('コンニチハ', text_util.reading('こんにちは'))
        self.assertEqual('フトンガフットンダ', text_util.reading('布団が吹っ飛んだ'))
        # with dict
        self.assertEqual('アルドゥイーノ', text_util.reading('Arduino'))
        # alphabet
        self.assertEqual('エービーシーディー', text_util.reading('ABCD'))
        self.assertEqual('', text_util.reading('abcd'))

    def test_正_形態素解析(self):
        # 通常の形態素解析
        self.assertEqual(['キョウ', 'ノ', 'テンキ'], text_util.convert_morphs('今日の天気'))
        # 助詞，助動詞フィルタリング
        self.assertEqual(['キョウ', 'テンキ'], text_util.convert_morphs('今日の天気', True))

    def test_正_ノイズフィルタリング(self):
        self.assertEqual('', text_util.remove_noise('!@#$%^^&*()，。/-_=+;:'))
        self.assertEqual('', text_util.remove_noise('🤗⭕🤓🤔🤘🦁⭐🆗🆖🈲🤐🤗🤖🤑🆙⏩'))
        self.assertEqual('布団が吹っ飛んだ', text_util.remove_noise('布団が吹っ飛んだwwwWWWｗｗｗＷＷＷ'))
        self.assertEqual('wwwwaa', text_util.remove_noise('wwwwaa'))
        self.assertEqual('布団が吹っ飛んだ', text_util.remove_noise('布団が吹っ飛んだ'))

    def test_正_n_gram(self):
        self.assertEqual(['あい', 'いう', 'うえ', 'えお'], text_util.n_gram('あいうえお', 2))
        self.assertEqual(['あいう', 'いうえ', 'うえお'], text_util.n_gram('あいうえお', 3))
        self.assertEqual(['あいうえ', 'いうえお'], text_util.n_gram('あいうえお', 4))
        self.assertEqual(['あいうえお'], text_util.n_gram('あいうえお', 5))

    def test_正_テキストの正規化(self):
        self.assertEqual('カキクケコ', text_util.normalize('ガギグゲゴ'))
        self.assertEqual('アイイ', text_util.normalize('アアアイイ'))

    def test_正_テキストを文字コードのベクトルに変換(self):
        text: str = 'こんにちは'
        self.assertEqual(
            [12371, 12435, 12395, 12385, 12399] + [0] * (config.TEXT_MAX_LENGTH - len(text)),
            text_util.vectorize(text)
        )
