import unittest

from core.model.dajare_model import DajareModel


class TestDajareModel(unittest.TestCase):
    def setUp(self):
        self.dajare = DajareModel()

    def test_正_テキストを代入(self):
        text = "布団が吹っ飛んだ"
        self.dajare.text = text
        self.assertEqual(text, self.dajare.text)

    def test_異_誤ったテキストを代入(self):
        with self.assertRaises(TypeError):
            self.dajare.text = None

    def test_正_判定結果を代入(self):
        is_dajare = True
        self.dajare.is_dajare = is_dajare
        self.assertEqual(is_dajare, self.dajare.is_dajare)

    def test_異_誤った判定結果を代入(self):
        with self.assertRaises(TypeError):
            self.dajare.is_dajare = None

    def test_正_スコアを代入(self):
        score = 3.0
        self.dajare.score = score
        self.assertEqual(score, self.dajare.score)

    def test_異_誤ったスコアを代入(self):
        with self.assertRaises(TypeError):
            self.dajare.score = None

        test_cases = [-1.0, 0.9, 5.1]
        for score in test_cases:
            with self.assertRaises(ValueError):
                self.dajare.score = score

    def test_正_読みを代入(self):
        reading = "布団が吹っ飛んだ"
        self.dajare.reading = reading
        self.assertEqual(reading, self.dajare.reading)

    def test_異_誤った読みを代入(self):
        with self.assertRaises(TypeError):
            self.dajare.reading = None

    def test_正_判定ルールを代入(self):
        applied_rule = "rule name"
        self.dajare.applied_rule = applied_rule
        self.assertEqual(applied_rule, self.dajare.applied_rule)

    def test_異_誤った判定ルールを代入(self):
        with self.assertRaises(TypeError):
            self.dajare.applied_rule = None
