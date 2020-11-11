import unittest


class TestAPI(unittest.TestCase):
    def setUp(self):
        from engine import text_service
        self.text_service = text_service

    def test_katakanize(self):
        self.assertEqual('コンニチハ', self.text_service.katakanize('こんにちは'))
