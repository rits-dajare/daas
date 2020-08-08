# -*- coding: utf-8 -*-
import unittest


class TestDajareJudge(unittest.TestCase):
    def setUp(self):
        from engine.judge_engine import JudgeEngine
        from reading.reading_service import ReadingService
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


class TestReading(unittest.TestCase):
    def setUp(self):
        from reading.reading_service import ReadingService
        self.converter = ReadingService()

    def test_convert_to_reading(self):
        text = 'こんにちは'
        # with api
        self.assertEqual('コンニチハ', self.converter.convert(text, True))
        # without api
        self.assertEqual('コンニチハ', self.converter.convert(text, False))


class TestSensitive(unittest.TestCase):
    def setUp(self):
        from sensitive.checker import SensitiveChecker
        self.checker = SensitiveChecker()

    def test_sensitive_tags(self):
        text = '殺人，麻薬'
        self.assertEqual(
            ['傷害', '恐喝', '殺人', '脅迫', '薬物', '覚せい剤', '麻薬'],
            self.checker.find_tags(text))


if __name__ == '__main__':
    unittest.main()
