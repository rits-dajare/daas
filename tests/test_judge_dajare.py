# -*- coding: utf-8 -*-
import unittest


class TestJudgeDajare(unittest.TestCase):
    def setUp(self):
        from engine.judge_engine import JudgeEngine
        from text.reading.reading_service import ReadingService
        converter = ReadingService()
        self.judge_engine = JudgeEngine(converter)

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
