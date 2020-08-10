# -*- coding: utf-8 -*-
import os
import re
from janome.tokenizer import Tokenizer
from kanjize import int2kanji
import collections
import jaconv
import pyboin
from . import engine


class JudgeEngine(engine.Engine):
    def _setup(self):
        self.tokenizer = Tokenizer()

        self.pass_pattern = self.__load_pass_pattern()
        self.not_pass_pattern = self.__load_not_pass_pattern()

    def is_dajare(self, text, use_api=True):
        # ダジャレとみなす
        if self.__force_pass(text):
            return True
        # ダジャレとみなさない
        if self.__not_pass(text):
            return False

        # textを読み/形態素に変換
        reading, morphs = self.__reading_and_morphs(text, use_api)
        reading, morphs = self.__nomalize(reading, morphs)

        return self.__rec_judge(reading, morphs, len(reading) >= 20)

    def __judge(self, reading, morphs, is_tight=False):
        # 2文字以上の形態素と同じ音が重複
        for m in morphs:
            if len(m) < 2:
                continue
            if reading.count(m) >= 2:
                return True

        # n-gramの重複を確認
        n_gram = [
            self.__n_gram(reading, 3),
            self.__n_gram(reading, 4),
        ]
        for char in n_gram:
            for i, ch1 in enumerate(char):
                for ch2 in char[(i+1):]:
                    if is_tight:
                        if self.__count_str_match(ch1, ch2) >= 3:
                            return True
                    else:
                        # 1文字一致
                        if self.__count_str_match(ch1, ch2) == 1:
                            if len(ch1) == 3:
                                if sorted(ch1) == sorted(ch2):
                                    return True
                        # 2文字一致
                        elif self.__count_str_match(ch1, ch2) >= 2:
                            # 母音一致
                            if sorted(pyboin.text2boin(ch1)) == sorted(pyboin.text2boin(ch2)):
                                return True
                            # 子音一致
                            if sorted([pyboin.romanize(ch, 'ア') for ch in ch1]) == \
                                    sorted([pyboin.romanize(ch, 'ア') for ch in ch2]):
                                return True

    def __rec_judge(self, reading, morphs, is_tight=False):
        if self.__judge(reading, morphs, is_tight):
            return True
        if is_tight:
            return False

        # パターンが含まれている場合，置換して再判定
        replace_pattern = [
            ['ー', ''],
            ['ッ', ''],
            ['ン', ''],
            ['イウ', 'ユー'],
        ]
        for pattern in replace_pattern:
            if pattern[0] in reading:
                if self.__rec_judge(
                        reading.replace(pattern[0], pattern[1]),
                        [m.replace(pattern[0], pattern[1]) for m in morphs],
                        is_tight):
                    return True

        # 母音を発音に変換
        vowel_pattern = [
            ['オウ', lambda ch: ch[0] + 'ー'],
            ['エイ', lambda ch: ch[0] + 'ー'],
        ]
        converted_reading = reading
        converted_morphs = morphs
        for bi_char in self.__n_gram(reading, 2):
            for sub in vowel_pattern:
                if pyboin.text2boin(bi_char[0]) + bi_char[1] == sub[0]:
                    converted_reading = converted_reading.replace(
                        bi_char, sub[1](bi_char))
                    converted_morphs = [
                        m.replace(bi_char, sub[1](bi_char)) for m in converted_morphs]
        if converted_reading != reading:
            if self.__rec_judge(converted_reading, converted_morphs, is_tight):
                return True

        # 小文字の直前文字を小文字の母音に変換
        # ex. 'シュン' -> 'スン'
        matches = re.findall(r'.[ァィゥェォャュョヮ]', reading)
        if matches != []:
            lower_to_vowel_reading = reading
            for ch in matches:
                lower_to_vowel_reading = lower_to_vowel_reading.replace(
                    ch,
                    pyboin.romanize(ch[0], pyboin.text2boin(ch[1]))
                )
            if self.__rec_judge(lower_to_vowel_reading, morphs, is_tight):
                return True

        return False

    def __reading_and_morphs(self, text, use_api=True):
        reading = ''
        morphs = []

        reading = self.to_reading(text, use_api)

        # 2文字以上の形態素のみ抽出
        for token in self.tokenizer.tokenize(text):
            if token.part_of_speech.split(',')[0] in ['名詞', '形容詞']:
                if len(token.reading) >= 2:
                    morphs.append(token.reading)

        return reading, morphs

    def __nomalize(self, reading, morphs):
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

        # 3回以上繰り返された文字を1文字に圧縮
        reading = re.sub(r'(.)\1{2,}', r'\1', reading)

        # 連続された母音の末尾をハイフンに変換
        for ci in range(len(reading) - 1):
            if reading[ci+1] not in 'アイウエオ':
                continue

            if pyboin.text2boin(reading[ci]) == \
                    pyboin.text2boin(reading[ci+1]):
                reading = reading[:ci+1] + 'ー' + reading[ci+2:]

        # 連続したハイフンを圧縮
        reading = re.sub(r'ー+', 'ー', reading)

        return reading, morphs

    def __n_gram(self, text, n):
        return [text[idx:idx + n] for idx in range(len(text) - n + 1)]

    def __count_str_match(self, s1, s2):
        count = 0
        for i in range(len(s1)):
            if s1[i] == s2[i]:
                count += 1

        return count

    def __not_pass(self, text):
        # 弾くパターン
        for pattern in self.not_pass_pattern:
            if re.search(pattern, text) is not None:
                return True

        text = self.exclude_noise(text)

        # 30文字以上
        if len(text) >= 30:
            return True
        # シンメトリー(xxx|xxx) & ABCDABCD パターン
        pivot = len(text) // 2
        if text[:pivot] == text[pivot + len(text) % 2:][::-1]:
            return True
        if text[:pivot] == text[pivot + len(text) % 2:]:
            return True
        # 同じ文字が6回以上使われている
        if collections.Counter(text).most_common()[0][1] >= 6:
            return True
        # アルファベットのみ
        if re.fullmatch(r'[\da-zA-Z,.]*', text) is not None:
            return True
        # [x, y]：文字がx種類以下 && 文字列がy文字以上
        chars_length_rules = [
            [4, 7],
            [5, 10],
        ]
        chars = [ch for ch in text]
        for rule in chars_length_rules:
            if len(set(chars)) <= rule[0] and len(text) >= rule[1]:
                return True

    def __force_pass(self, text):
        for pattern in self.pass_pattern:
            if re.search(pattern, text) is not None:
                return True

        return False

    def __load_pass_pattern(self):
        result = []
        with open('config/pass_pattern.txt') as f:
            result = f.read().split('\n')
            result.remove('')

        return result

    def __load_not_pass_pattern(self):
        result = []
        with open('config/not_pass_pattern.txt') as f:
            result = f.read().split('\n')
            result.remove('')

        return result
