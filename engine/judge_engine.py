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
from engine import engine
# --------------------------------------------------------------------------------------


class JudgeEngine(engine.Engine):
    def __init__(self):
        super().__init__()
        self.tokenizer = Tokenizer()

    def is_dajare(self, dajare, use_api=True):
        # force pass as dajare
        for pattern in self.force_judge_pattern:
            if re.match(pattern, dajare) is not None:
                return True

        # not pass symmetry(xxx|xxx) pattern
        # ex. テストテスト -> not dajare
        pivot = len(dajare) // 2
        if dajare[:pivot] == dajare[pivot:]:
            return False

        # convert dajare to reading & morphs
        reading, morphs = self.to_reading_and_morphs(dajare, use_api)
        reading, morphs = self.preprocessing(reading, morphs)

        # only ~x chars are used & length >= y -> not dajare
        # [x, y]  x: chars, y: length
        chars_length_rules = [
            [3, float('inf')],
            [4, 7],
            [5, 10]
        ]
        chars = [ch for ch in dajare]
        for rule in chars_length_rules:
            if len(set(chars)) <= rule[0] and len(dajare) >= rule[1]:
                return False

        # tri-gram is matched
        tri_gram = self.n_gram(reading, 3)
        if len(set(tri_gram)) != len(tri_gram):
            return True

        if self.judge(reading, morphs):
            return True

        return False

    def judge(self, reading, morphs):
        # whether morph is included multiple
        for m in morphs:
            if reading.count(m) >= 2:
                return True

        # whether judgment rules holds
        tri_char = self.n_gram(reading, 3)

        for i, tri1 in enumerate(tri_char):
            for tri2 in tri_char[(i+1):]:
                # all match
                if tri1 == tri2:
                    return True

                # 2 chars match && all vowels match
                if self.count_str_match(tri1, tri2) == 2:
                    if pyboin.text2boin(tri1) == pyboin.text2boin(tri2):
                        return True

        # exclude 'ー'
        if 'ー' in reading:
            if self.judge(reading.replace('ー', ''), morphs):
                return True

        # exclude 'ッ'
        if 'ッ' in reading:
            if self.judge(reading.replace('ッ', ''), [m.replace('ッ', '') for m in morphs]):
                return True

        # convert vowel text to pronunciation
        vowel_pattern = [
            ['オウ', lambda ch: ch[0] + 'ー'],
            ['エイ', lambda ch: ch[0] + 'ー'],
        ]
        converted_reading = reading
        converted_morphs = morphs
        for bi_char in self.n_gram(reading, 2):
            for sub in vowel_pattern:
                if pyboin.text2boin(bi_char[0]) + bi_char[1] == sub[0]:
                    converted_reading = converted_reading.replace(bi_char, sub[1](bi_char))
                    converted_morphs = [m.replace(bi_char, sub[1](bi_char)) for m in converted_morphs]
        if converted_reading != reading:
            if self.judge(converted_reading, converted_morphs):
                return True

        # 'イウ' -> 'ユー'
        if 'イウ' in reading:
            if self.judge(reading.replace('イウ', 'ユー'), [m.replace('イウ', 'ユー') for m in morphs]):
                return True

        # convert char to next lower's vowel
        # ex. 'シュン' -> 'スン'
        matches = re.findall(r'.[ァィゥェォャュョヮ]', reading)
        if matches != []:
            lower_to_vowel_reading = reading
            for ch in matches:
                lower_to_vowel_reading = lower_to_vowel_reading.replace(
                    ch,
                    pyboin.romanize(ch[0], pyboin.text2boin(ch[1]))
                )
            if self.judge(lower_to_vowel_reading, morphs):
                return True

        return False

    def to_reading_and_morphs(self, dajare, use_api=True):
        reading = ''
        morphs = []

        # use docomo api
        if use_api:
            reading = self.to_reading(dajare)

        # not use api || cannot use api
        if reading == '':
            for ch in re.findall('\d+', dajare):
                dajare = dajare.replace(ch, int2kanji(int(ch)))

            # morphological analysis
            for token in self.tokenizer.tokenize(dajare):
                if token.reading == '*':
                    # token with unknown word's reading
                    reading += jaconv.hira2kata(token.surface)
                else:
                    # token with known word's reading
                    reading += token.reading

                # extract morphs (len >= 2)
                if len(token.reading) >= 2:
                    morphs.append(token.reading)

        # extract morphs (len >= 2)
        if morphs == []:
            for token in self.tokenizer.tokenize(dajare):
                if len(token.reading) >= 2:
                    morphs.append(token.reading)

        # force convert reading
        reading = jaconv.hira2kata(reading)

        # exclude noises
        reading = ''.join(re.findall('[ァ-ヴー]+', reading))

        return reading, morphs

    def preprocessing(self, reading, morphs):
        # nomalize text
        nomalize_pair = [
            'ヲヂガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ',
            'オジカキクケコサシスセソタチツテトハヒフヘホハヒフヘホ'
        ]
        for i in range(len(nomalize_pair[0])):
            reading = reading.replace(
                nomalize_pair[0][i],
                nomalize_pair[1][i],
            )
            morphs = [m.replace(
                nomalize_pair[0][i],
                nomalize_pair[1][i]) for m in morphs]

        # exclude 3~ times looped chars
        reading = re.sub(r'(.)\1{2,}', r'\1', reading)

        # convert looped vowel text to '-'
        for ci in range(len(reading) - 1):
            if reading[ci+1] not in 'アイウエオ':
                continue

            if pyboin.text2boin(reading[ci]) == \
                    pyboin.text2boin(reading[ci+1]):
                reading = reading[:ci+1] + 'ー' + reading[ci+2:]

        # unified looped hyphen
        reading = re.sub(r'ー+', 'ー', reading)

        return reading, morphs

    def n_gram(self, dajare, n):
        return [dajare[idx:idx + n] for idx in range(len(dajare) - n + 1)]

    def count_str_match(self, s1, s2):
        count = 0
        for i in range(len(s1)):
            if s1[i] == s2[i%len(s2)]:
                count += 1

        return count

