import unittest

from core import message
from core.service.dajare_service import DajareService


class TestEngine(unittest.TestCase):
    def setUp(self):
        self.dajare_service = DajareService()

    def test_正_ダジャレを判定(self):
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
            [True, 'コーンが真横ーン'],
            [True, '打倒だと〜'],
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
            [False, '麻生「あっそ」'],
            [False, 'AはAだ'],
            [False, 'ああいあい'],
            [False, 'テストあいうテストかきく'],
            [False, 'あいうえあいうえ-あ'],
            [False, 'あいうえおあいうえお-あ'],
            [False, 'フトンガフットンダ'],
        ]
        for case in cases:
            dajare = self.dajare_service.judge_dajare(case[1])
            try:
                self.assertEqual(
                    case[0],
                    dajare.is_dajare
                )
            except AssertionError as error:
                print(message.APPLIED_RULE(case[1], dajare.applied_rule))
                raise error

    def test_正_ダジャレを評価(self):
        dajare = self.dajare_service.eval_dajare('布団が吹っ飛んだ')
        self.assertTrue(dajare.score >= 1.0 and dajare.score <= 5.0)

    def test_正_ダジャレを読みに変換(self):
        dajare = self.dajare_service.convert_reading('こんにちは')
        self.assertEqual(
            'コンニチハ',
            dajare.reading
        )
