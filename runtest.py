# -*- coding: utf-8 -*-

import unittest


class TestDajareJudge(unittest.TestCase):
    def setUp(self):
        from engine.judge_engine import JudgeEngine
        self.judge_engine = JudgeEngine()

    def test_to_reading(self):
        text = 'こんにちは'
        self.assertEqual('コンニチハ', self.judge_engine.to_reading(text))

    def test_exclude_noises(self):
        text = '!@#$%^^&*()，。/-_=+;:こんにちは'
        self.assertEqual('こんにちは', self.judge_engine.exclude_noise(text))

    def test_judge_dajare(self):
        texts = [
            [True, '布団が吹っ飛んだ'],
            [True, '紅茶が凍っちゃった'],
            [True, 'ダジャレを言うのは誰じゃ'],
            [False, 'テストテスト'],
            [True, 'ニューヨークで入浴'],
            [True, '芸夢なゲーム'],
            [True, '臭いサイ'],
        ]
        for text in texts:
            self.assertEqual(
                text[0], self.judge_engine.is_dajare(text[1], False))

    def test_n_gram(self):
        text = 'こんにちは。'
        self.assertEqual(
            ['こん', 'んに', 'にち', 'ちは', 'は。'],
            self.judge_engine.n_gram(text, 2))
        self.assertEqual(
            ['こんに', 'んにち', 'にちは', 'ちは。'],
            self.judge_engine.n_gram(text, 3))


class TestReading(unittest.TestCase):
    def setUp(self):
        from reading.withapi import WithAPI
        from reading.withoutapi import WithoutAPI
        self.conv_with_api = WithAPI()
        self.conv_without_api = WithoutAPI()

    def test_convert_with_api(self):
        text = 'こんにちは'
        self.assertEqual('コンニチハ', self.conv_with_api.text_to_reading(text)[0])

    def test_convert_without_api(self):
        text = 'こんにちは'
        self.assertEqual('コンニチハ', self.conv_without_api.text_to_reading(text)[0])


if __name__ == '__main__':
    unittest.main()
