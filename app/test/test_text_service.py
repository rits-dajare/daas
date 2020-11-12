import unittest


class TestAPI(unittest.TestCase):
    def setUp(self):
        from engine import text_service
        self.text_service = text_service

    def test_katakanize(self):
        text = 'こんにちは'
        self.assertEqual('コンニチハ', self.text_service.katakanize(text, False))

    def test_morphs(self):
        text = 'こんにちは世界'
        self.assertEqual(['コンニチハ', 'セカイ'], self.text_service.morphs(text))

    def test_cleaned(self):
        text = '!@#$%^^&*()，。/-_=+;:こんにちはwww'
        self.assertEqual('こんにちは', self.text_service.cleaned(text))

    def test_count_char_matches(self):
        self.assertEqual(0, self.text_service.count_char_matches('ABC', 'BCA'))
        self.assertEqual(1, self.text_service.count_char_matches('ABC', 'ACB'))
        self.assertEqual(2, self.text_service.count_char_matches('ABC', 'ABB'))
        self.assertEqual(3, self.text_service.count_char_matches('ABC', 'ABC'))

    def test_n_gram(self):
        self.assertEqual(['こんに', 'んにち', 'にちは'],
                         self.text_service.n_gram('こんにちは', 3))

    def test_nomalize(self):
        self.assertEqual('カキクケコ', self.text_service.normalize('ガギグゲゴ'))
