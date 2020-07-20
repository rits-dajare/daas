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
import emoji
from engine import engine
# --------------------------------------------------------------------------------------


class JudgeEngine(engine.Engine):
    def __init__(self):
        super().__init__()
        self.tokenizer = Tokenizer()

    def is_dajare(self, dajare, use_api=True):
        # force pass as dajare
        for pattern in self.force_judge_pattern:
            if re.search(pattern, dajare) is not None:
                return True

        # not pass symmetry(xxx|xxx) & ABCDABCD pattern
        # ex. テストテスト -> not dajare
        pivot = len(dajare) // 2
        if dajare[:pivot] == dajare[pivot + len(dajare)%2:]:
            return False
        if dajare[:pivot] == dajare[pivot + len(dajare)%2:][::-1]:
            return False

        # not pass only alphabet chars
        if re.fullmatch(r'[a-zA-Z 　]*', dajare) is not None:
            return False

        # convert dajare to reading & morphs
        reading, morphs = self.to_reading_and_morphs(dajare, use_api)
        reading, morphs = self.preprocessing(reading, morphs)

        # not pass only ~x chars are used & length >= y
        # [x, y]  x: chars, y: length
        chars_length_rules = [
            [3, 0],
            [4, 7],
            [5, 10]
        ]
        chars = [ch for ch in reading]
        for rule in chars_length_rules:
            if len(set(chars)) <= rule[0] and len(dajare) >= rule[1]:
                return False

        # not pass ~4 length pattern
        if len(reading) <= 4:
            return False

        # tri-gram is matched
        tri_gram = self.n_gram(reading, 3)
        if len(set(tri_gram)) != len(tri_gram):
            return True

        if self.judge(reading, morphs):
            return True

        return False

    def judge(self, reading, morphs):
        # whether judgment rules holds ===================================
        # whether morph is included multiple
        for m in morphs:
            if reading.count(m) >= 2:
                return True

        # whether the divided readings match
        # tri-gram
        tri_char = self.n_gram(reading, 3)
        four_char = self.n_gram(reading, 4)

        for char in [tri_char, four_char]:
            for i, ch1 in enumerate(char):
                for ch2 in char[(i+1):]:
                    # only vewel -> not dajare
                    if re.fullmatch(r'[あいうえおぁぃぅぇぉアイウエオァィゥェォ]+', ch1) and \
                            re.fullmatch(r'[あいうえおぁぃぅぇぉアイウエオァィゥェォ]+', ch2):
                        continue

                    # 1 char match
                    if self.count_str_match(ch1, ch2) == 1:
                        if sorted(ch1) == sorted(ch2):
                            return True

                    # 2~ chars match
                    elif self.count_str_match(ch1, ch2) >= 2:
                        # all vowels match
                        if sorted(pyboin.text2boin(ch1)) == sorted(pyboin.text2boin(ch2)):
                            return True
                        #all consonant match
                        if sorted([pyboin.romanize(ch, 'ア') for ch in ch1]) == \
                                sorted([pyboin.romanize(ch, 'ア') for ch in ch2]):
                            return True
        # ================================================================

        # exclude 'ー'
        if 'ー' in reading:
            if self.judge(reading.replace('ー', ''), [m.replace('ー', '') for m in morphs]):
                return True

        # exclude 'ッ'
        if 'ッ' in reading:
            if self.judge(reading.replace('ッ', ''), [m.replace('ッ', '') for m in morphs]):
                return True

        # exclude 'ン'
        if 'ン' in reading:
            if self.judge(reading.replace('ン', ''), [m.replace('ン', '') for m in morphs]):
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
            'ヲヂガギグゲゴザジズゼゾダヂヅデドバビブヴベボパピプペポ',
            'オジカキクケコサシスセソタチツテトハヒフフヘホハヒフヘホ'
        ]
        for i in range(len(nomalize_pair[0])):
            reading = reading.replace(
                nomalize_pair[0][i],
                nomalize_pair[1][i],
            )
            morphs = [m.replace(
                nomalize_pair[0][i],
                nomalize_pair[1][i]) for m in morphs]

        # exclude emoji
        reading = ''.join([ch for ch in reading if ch not in emoji.UNICODE_EMOJI])

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
            if s1[i] == s2[i]:
                count += 1

        return count

