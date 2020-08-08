# -*- coding: utf-8 -*-
import os
from janome.tokenizer import Tokenizer
from reading.converter import Converter


class WithoutAPI(Converter):
    def _setup(self):
        self.tokenizer = Tokenizer()

    def _convert_reading(self, text):
        result = ''

        for token in self.tokenizer.tokenize(text):
            if token.reading == '*':
                # token with unknown word's reading
                result += token.surface
            else:
                # token with known word's reading
                result += token.reading

        return result, True
