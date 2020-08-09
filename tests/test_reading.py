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

    def test_convert_eng_word_to_reading(self):
        texts = [
            ['エービーシーディー', 'ABCD'],
            ['エービーシー', 'ABC'],
            ['', 'abcd'],
            ['ハロー', 'hello'],
        ]
        for text in texts:
            self.assertEqual(
                text[0],
                self.converter.convert(text[1])
            )
