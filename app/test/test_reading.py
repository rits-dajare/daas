# -*- coding: utf-8 -*-
import unittest
from engine.api import *


class TestReading(unittest.TestCase):
    def test_convert_to_reading(self):
        text = 'こんにちは'
        # with api
        self.assertEqual('コンニチハ', reading_converter.convert(text, True))
        # without api
        self.assertEqual('コンニチハ', reading_converter.convert(text, False))

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
                reading_converter.convert(text[1])
            )
