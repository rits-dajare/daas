# -*- coding: utf-8 -*-

import unittest
from engine.judge_engine import JudgeEngine


class TestDajare(unittest.TestCase):
    def test_to_reading(self):
        judge_engine = JudgeEngine()
        text = 'こんにちは'
        self.assertEqual('コンニチハ', judge_engine.to_reading(text))

    def test_exclude_noises(self):
        judge_engine = JudgeEngine()
        text = '!@#$%^^&*()，。/-_=+;:こんにちは'
        self.assertEqual('こんにちは', judge_engine.exclude_noise(text))

    def test_judge_dajare(self):
        judge_engine = JudgeEngine()
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
            self.assertEqual(text[0], judge_engine.is_dajare(text[1], False))

    def test_n_gram(self):
        judge_engine = JudgeEngine()
        text = 'こんにちは。'
        self.assertEqual(
            ['こん', 'んに', 'にち', 'ちは', 'は。'],
            judge_engine.n_gram(text, 2))
        self.assertEqual(
            ['こんに', 'んにち', 'にちは', 'ちは。'],
            judge_engine.n_gram(text, 3))


if __name__ == '__main__':
    unittest.main()
