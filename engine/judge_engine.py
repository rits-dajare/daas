# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------
import sys
from pathlib import Path
sys.path.append(str(Path('__file__').resolve().parent))
# --------------------------------------------------------------------------------------
import os
import re
from janome.tokenizer import Tokenizer
from kanjize import int2kanji
import jaconv
import pyboin
import engine
# --------------------------------------------------------------------------------------


class JudgeEngine(engine.Engine):
    def __init__(self):
        self.tokenize = Tokenizer()

    def to_reading_and_morphemes(self, dajare, use_api=True):
        reading = ''

        # use docomo api
        if use_api:
            reading = self.to_reading(dajare)

        # not use api || cannot use api
        if reading == '':
            for ch in re.findall('\d+', dajare):
                dajare = dajare.replace(ch, int2kanji(int(ch)))

            # morphological analysis
            for token in self.tokenize.tokenize(dajare):
                reading = token.reading

                if reading == '*':
                    # token with unknown word's reading
                    reading += jaconv.hira2kata(token.surface)
                else:
                    # token with known word's reading
                    reading += reading

        # extract morphemes (len >= 2)
        morphemes = []
        for token in self.tokenize.tokenize(dajare):
            if len(token.reading) >= 2:
                morphemes.append(token.reading)

        # force convert reading
        reading = jaconv.hira2kata(reading)

        # exclude noises
        reading = ''.join(re.findall('[ァ-ヴー]+', reading))

        return reading, morphemes

    def n_gram(self, dajare, n):
        return [dajare[idx:idx + n] for idx in range(len(dajare) - n + 1)]


judge_engine = JudgeEngine()
print(judge_engine.to_reading_and_morphemes('布団が吹っ飛んだ'))
