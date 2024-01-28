import unittest
from parameterized import parameterized

from app.service.dajare_service import DajareService


class TestDajareService(unittest.TestCase):
    def setUp(self):
        self.dajare_service = DajareService()

    @parameterized.expand([
        # __force_pass
        [True, 'この卵エッグ'],
        [True, '車かぁ'],
        # __pass_full_match
        [True, 'トイレに行っといれ'],
        # __pass_morphs_overlap
        [True, '臭いサイ'],
        # __pass_vowel_match
        [True, 'アヒージョはアチーよ'],
        # __pass_consonant_match
        [True, 'サイゼで見た彗星'],
        # __pass_swap_match
        [True, 'ダジャレを言うのは誰じゃ'],
        # __pass_magic_nn
        [True, '南下するけど何か？'],
        # __conv_with_pattern
        [True, '布団が吹っ飛んだ'],
        # __conv_vowel_to_pron
        [True, '紅茶が凍っちゃった'],
        # __conv_looped_vowel_to_hyphen
        [True, '芸無なゲーム'],
        [True, '打倒だと〜'],
        [True, 'ニューヨークで入浴'],
        # __conv_prev_of_lower_ch_to_vowel
        [True, 'ローソンのローション'],
        # __reject_length
        [False, '布団が吹っ飛んだこの焼き肉は焼きにくいダジャレを言うのは誰じゃ'],
        # __reject_force_patterns
        [False, '麻生「あっそ」'],
        # __reject_only_katakana
        [False, 'フトンガフットンダ'],
        [False, 'レイヤーオブザイヤー'],
        # __reject_ch_many_times_used
        [False, '布団が吹っ飛んだだだだだだ'],
        # __reject_only_used_alphanumeric
        [False, 'ABCDEFGHIJK'],
        # __reject_block_many_times_used
        [False, 'トイレに行っトイレ'],
        # __reject_2_ch_match
        [False, '野球は野球だ'],
        [True, '同棲買い出しに、どう正解出し？'],
        [True, 'コーンが真横ーン'],
        # __reject_lapel_pattern
        [False, 'ダジャレダジャレ'],
        # others
        [False, '判定テストです'],
    ])
    def test_正_ダジャレを判定(self, is_dajare: bool, text: str):
        dajare = self.dajare_service.judge_dajare(text)
        self.assertEqual(
            is_dajare,
            dajare.is_dajare
        )

    def test_正_ダジャレを評価(self):
        dajare = self.dajare_service.eval_dajare('布団が吹っ飛んだ')
        self.assertTrue(dajare.score >= 1.0 and dajare.score <= 5.0)

    def test_正_ダジャレを読みに変換(self):
        dajare = self.dajare_service.convert_reading('布団が吹っ飛んだ')
        self.assertEqual(
            'フトンガフットンダ',
            dajare.reading
        )
