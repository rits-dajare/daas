# -*- coding: utf-8 -*-
import unittest


class TestSensitive(unittest.TestCase):
    def setUp(self):
        from text.sensitive.checker import SensitiveChecker
        self.checker = SensitiveChecker()

    def test_sensitive_tags(self):
        text = '殺人，麻薬'
        self.assertEqual(
            ['傷害', '恐喝', '殺人', '脅迫', '薬物', '覚せい剤', '麻薬'],
            self.checker.find_tags(text))
