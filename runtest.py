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
