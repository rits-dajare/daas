import unittest

from core.model import dajare_model


class TestDajareModel(unittest.TestCase):
    def setUp(self):
        self.dajare = dajare_model.DajareModel()

    def test_正_テキストを代入(self):
        text = "布団が吹っ飛んだ"
        self.dajare.text = text
        self.assertEqual(text, self.dajare.text)

    def test_異_誤ったテキストを代入(self):
        with self.assertRaises(TypeError):
            self.dajare.text = None

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
