# -*- coding: utf-8 -*-
import unittest


class TestReading(unittest.TestCase):
    def setUp(self):
        from text.reading.reading_service import ReadingService
        self.converter = ReadingService()

    def test_convert_to_reading(self):
        text = 'こんにちは'
        # with api
        self.assertEqual('コンニチハ', self.converter.convert(text, True))
        # without api
        self.assertEqual('コンニチハ', self.converter.convert(text, False))
