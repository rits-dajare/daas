# -*- coding: utf-8 -*-
import unittest
from engine.api import *


class TestSensitive(unittest.TestCase):
    def test_sensitive_tags(self):
        text = '殺人，麻薬'
        self.assertEqual(
            ['傷害', '恐喝', '殺人', '脅迫', '薬物', '覚せい剤', '麻薬'],
            sensitive_checker.find_tags(text))
