# -*- coding: utf-8 -*-
import os
import re
from janome.tokenizer import Tokenizer
from kanjize import int2kanji
import jaconv
import pyboin
from engine import engine


class JudgeEngine(engine.Engine):
    def _setup(self):
        self.tokenizer = Tokenizer()

        self.pass_pattern = self.__load_pass_pattern()

    def is_dajare(self, dajare, use_api=True):
        # force pass as dajare
        if self.__force_pass(dajare):
            return True

        dajare_cleaned = self.exclude_noise(dajare)

        # not pass 30~ chars
        if len(dajare_cleaned) >= 30:
            return False

        # not pass symmetry(xxx|xxx) & ABCDABCD pattern
        # ex. テストテスト -> not dajare
        pivot = len(dajare_cleaned) // 2
        if dajare_cleaned[:pivot] == dajare_cleaned[pivot + len(dajare) % 2:]:
            return False
        if dajare_cleaned[:pivot] == dajare_cleaned[pivot + len(dajare) % 2:][::-1]:
            return False

        # not pass only alphabet chars
        if re.fullmatch(r'[\da-zA-Z 　,]*', dajare_cleaned) is not None:
            return False

        # not pass xxxoxxxo(x: not hiragana, o: hiragana) pattern
        if re.fullmatch(r'[^\u3041-\u3096]+[\u3041-\u3096]*[^\u3041-\u3096]+[\u3041-\u3096]*', dajare_cleaned) is not None:
            noise = re.compile(r'[\u3041-\u3096]')
            tmp_dajare = noise.sub('', dajare_cleaned)
            pivot = len(tmp_dajare) // 2
            if tmp_dajare[:pivot] == tmp_dajare[pivot:]:
                return False

        # not pass only ~x chars are used & length >= y
        # [x, y]  x: chars, y: length
        chars_length_rules = [
            [3, 0],
            [4, 7],
            [5, 10]
        ]
        chars = [ch for ch in dajare_cleaned]
        for rule in chars_length_rules:
            if len(set(chars)) <= rule[0] and len(dajare_cleaned) >= rule[1]:
                return False

        # convert dajare to reading & morphs
        reading, morphs = self.to_reading_and_morphs(dajare, use_api)
        reading, morphs = self.preprocessing(reading, morphs)

        return self.judge(reading, morphs, len(reading) >= 20)

    def judge(self, reading, morphs, is_tight=False):
        # whether judgment rules holds ===================================
        # whether morph is included multiple
        for m in morphs:
            if len(m) < 2:
                continue
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

                    if is_tight:
                        if self.count_str_match(ch1, ch2) >= 3:
                            if ch1.count('ー') < 2:
                                return True
                    else:
                        # 1 char match
                        if self.count_str_match(ch1, ch2) == 1:
                            if len(ch1) == 3:
                                if sorted(ch1) == sorted(ch2):
                                    return True

                        # 2~ chars match
                        elif self.count_str_match(ch1, ch2) >= 2:
                            # all vowels match
                            if sorted(pyboin.text2boin(ch1)) == sorted(pyboin.text2boin(ch2)):
                                return True
                            # all consonant match
                            if sorted([pyboin.romanize(ch, 'ア') for ch in ch1]) == \
                                    sorted([pyboin.romanize(ch, 'ア') for ch in ch2]):
                                return True
        # ================================================================

        if is_tight:
            return False

        # exclude 'ー'
        if 'ー' in reading:
            if self.judge(reading.replace('ー', ''), [m.replace('ー', '') for m in morphs], is_tight):
                return True

        # exclude 'ッ'
        if 'ッ' in reading:
            if self.judge(reading.replace('ッ', ''), [m.replace('ッ', '') for m in morphs], is_tight):
                return True

        # exclude 'ン'
        if 'ン' in reading:
            if self.judge(reading.replace('ン', ''), [m.replace('ン', '') for m in morphs], is_tight):
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
                    converted_reading = converted_reading.replace(
                        bi_char, sub[1](bi_char))
                    converted_morphs = [
                        m.replace(bi_char, sub[1](bi_char)) for m in converted_morphs]
        if converted_reading != reading:
            if self.judge(converted_reading, converted_morphs, is_tight):
                return True

        # 'イウ' -> 'ユー'
        if 'イウ' in reading:
            if self.judge(reading.replace('イウ', 'ユー'), [m.replace('イウ', 'ユー') for m in morphs], is_tight):
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
            if self.judge(lower_to_vowel_reading, morphs, is_tight):
                return True

        return False

    def to_reading_and_morphs(self, text, use_api=True):
        reading = ''
        morphs = []

        reading = self.to_reading(text, use_api)

        # extract morphs (len >= 2)
        for token in self.tokenizer.tokenize(text):
            if token.part_of_speech.split(',')[0] in ['名詞', '形容詞']:
                if len(token.reading) >= 2:
                    morphs.append(token.reading)

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

    def n_gram(self, text, n):
        return [text[idx:idx + n] for idx in range(len(text) - n + 1)]

    def count_str_match(self, s1, s2):
        count = 0
        for i in range(len(s1)):
            if s1[i] == s2[i]:
                count += 1

        return count

    def __force_pass(self, text):
        for pattern in self.pass_pattern:
            if re.search(pattern, text) is not None:
                return True
        return False

    def __load_pass_pattern(self):
        result = []
        with open('config/force_judge_pattern.txt') as f:
            result = f.read().split('\n')
            result.remove('')

        return result
