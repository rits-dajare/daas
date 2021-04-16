import unittest

from core import engine
from core import message


class TestEngine(unittest.TestCase):
    def test_judge_dajare(self):
        cases = [
            [True, '布団が吹っ飛んだ'],
            [True, '芸無なゲーム'],
            [True, 'ダジャレを言うのは誰じゃ'],
            [True, '紅茶が凍っちゃった'],
            [True, 'ニューヨークで入浴'],
            [True, 'アヒージョはアチーよ'],
            [True, '臭いサイ'],
            [True, 'サイゼで見た彗星'],
            [True, '南下するけど何か？'],
            [True, '同棲買い出しに、どう正解出し？'],
            [True, 'この卵エッグ'],
            [True, 'かきくけあカキエク-ん'],
            [True, 'かきくけあカキケク-ん'],
            [True, 'かきくあカキック-んン'],
            [True, 'かきくあカキンク-んン'],
            [True, 'かきくあカキーク-んン'],
            [True, 'かきいあカキー-んン'],
            [True, 'かこうあカコー-んン'],
            [True, 'かけいあカケー-んン'],
            [True, 'しゃんあサンア'],
            [False, 'あいうあいう-ん'],
            [False, 'あいあいあいあいあいあい-かきくけこ'],
            [False, '布団が吹っ飛んだ布団が吹っ飛んだあいうえおかきくけこさしすせ'],
            [False, '判定テストです'],
            [False, '野球は野球だ'],
            [False, 'AはAだ'],
            [False, 'ああいあい'],
            [False, 'テストあいうテストかきく'],
            [False, 'あいうえあいうえ-あ'],
            [False, 'あいうえおあいうえお-あ'],
            [False, 'フトンガフットンダ'],
        ]
        for case in cases:
            try:
                self.assertEqual(
                    case[0],
                    engine.judge_engine.exec(case[1])
                )
            except AssertionError as error:
                print(message.APPLIED_RULE(case[1], engine.judge_engine.applied_rule))
                raise error

    def test_eval(self):
        score = engine.eval_engine.exec('布団が吹っ飛んだ')
        self.assertTrue(score >= 1.0 and score <= 5.0)

    def test_reading(self):
        self.assertEqual(
            'コンニチハ',
            engine.reading_engine.exec('こんにちは')
        )
