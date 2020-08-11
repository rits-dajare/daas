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
            [True, '芸無なゲーム'],
            [True, 'ダジャレを言うのは誰じゃ'],
            [True, '紅茶が凍っちゃった'],
            [True, 'ニューヨークで入浴'],
            [True, '臭いサイ'],
            [True, 'この卵エッグ'],
            [True, 'かきくカケク'],
            [True, 'かきあカキァ'],
            [True, 'かきくサキク'],
            [True, 'かきくケキク'],
            [True, 'かきくけカキエク-ん'],
            [True, 'かきくけカキケク-ん'],
            [True, 'かきくカキック-んン'],
            [True, 'かきくカキンク-んン'],
            [True, 'かきくカキーク-んン'],
            [True, 'かきいカキー-んン'],
            [True, 'かこうカコー-んン'],
            [True, 'かけいカケー-んン'],
            [True, 'あいうアユー'],
            [True, 'しゃんあサンア'],
            [False, 'あいうあいう-ん'],
            [False, 'あいあいあいあいあいあい-かきくけこ'],
            [False, '布団が吹っ飛んだ布団が吹っ飛んだあいうえおかきくけこさしすせ'],
            [False, 'See you later, alligator'],
            [False, '野球は野球だ'],
            [False, 'あいうえあいうえ-あ'],
            [False, 'あいうえおあいうえお-あ'],
        ]
        for text in texts:
            self.assertEqual(
                text[0],
                self.judge_engine.is_dajare(text[1], False)
            )
