import sys
import re
import pyboin
import collections

from core import config
from core.util import text_util


class JudgeEngine:
    def __init__(self):
        self.pass_patterns = self.__load_patterns(config.JUDGE_PASS_DICT_PATH)
        self.reject_patterns = self.__load_patterns(config.JUDGE_REJECT_DICT_PATH)

        # no normalized reading
        self.ori_reading: str

        # applied method name
        self.applied_rule: str

        # text processing index
        self.text_proc_index: int

    def exec(self, text: str) -> bool:
        self.applied_rule = ''
        self.text_proc_index = 0

        # preprocessing
        text = text_util.filtering(text)
        # convert reading & morphs
        reading: str = text_util.reading(text)
        self.ori_reading = reading
        reading = text_util.normalize(reading)
        morphs: list = text_util.convert_morphs(text, True)
        morphs = [text_util.normalize(morph) for morph in morphs]

        # force judge
        if self.__force_reject(text):
            return False
        if self.__force_pass(text):
            return True

        return self.__rec_judge(reading, morphs, len(reading) >= config.TIGHT_LENGTH)

    def __judge(self, reading, morphs, is_tight=False):
        methods = [
            # 2文字以上の形態素が一致
            self.__rule_morphs_overlap,
            # 3文字完全一致
            self.__rule_full_match,
            # 母音完全一致
            self.__rule_vowel_match,
            # 子音完全一致
            self.__rule_consonant_match,
            # 文字が入れ替わっている
            self.__rule_swap_match,
            # 'ン'は全ての文字にマッチする
            self.__rule_magic_nn,
        ]

        for method in methods:
            if method(reading, morphs, is_tight):
                self.applied_rule = method.__name__
                return True

        return False

    def __rec_judge(self, reading, morphs, is_tight=False):
        if self.__judge(reading, morphs, is_tight):
            return True
        if is_tight:
            return False

        # increment loop index
        self.text_proc_index += 1

        methods = [
            # 単純なパターンで置換
            self.__conv_with_pattern,
            # 母音を発音に変換
            self.__conv_vowel_to_pron,
            # 連続された母音の末尾をハイフンに変換
            self.__conv_looped_vowel_to_hyphen,
            # 小文字の直前文字を小文字の母音に変換
            # ex. 'シュン' -> 'スン'
            self.__conv_prev_of_lower_ch_to_vowel,
        ]

        for method in methods:
            conv_reading, conv_morphs = method(reading, morphs)
            if conv_reading != reading:
                if self.__rec_judge(conv_reading, conv_morphs, is_tight):
                    return True

        return False

    def __force_pass(self, text):
        for pattern in self.pass_patterns:
            if re.search(pattern, text) is not None:
                self.applied_rule = sys._getframe().f_code.co_name
                return True

        return False

    def __force_reject(self, text):
        methods = [
            # 30文字以上
            self.__reject_length,
            # 強制的に弾くパターン
            self.__reject_force_patterns,
            # カタカナのみ
            self.__reject_only_katakana,
            # 同じ文字が6回以上使われている
            self.__reject_ch_many_times_used,
            # 半角文字のみ
            self.__reject_only_used_alphanumeric,
            # 同じひらがな/カタカナのブロックが重複
            self.__reject_block_many_times_used,
            # 同じ2文字が含まれている
            self.__reject_2_ch_match,
            # 折り返し（ABCD|ABCD）パターン
            self.__reject_lapel_pattern,
            # 文字がx種類以下 && 文字列がy文字以上
            self.__reject_len_of_sentence_and_ch,
        ]

        for method in methods:
            if method(text):
                self.applied_rule = method.__name__
                return True

        return False

    def __load_patterns(self, file):
        result = []
        with open(file, 'r') as f:
            result = f.read().split('\n')
            result.remove('')

        return result

    def __text_to_char_pair(self, reading, n=3):
        result = []
        n_gram = text_util.n_gram(reading, n)
        for i, ch1 in enumerate(n_gram):
            for ch2 in n_gram[i + 1:]:
                ch_index = [i for i, ch in enumerate(n_gram) if ch == ch1]
                if ch1 != ch2:
                    result.append([ch1, ch2])
                else:
                    if abs(ch_index[0] - ch_index[-1]) > 2:
                        result.append([ch1, ch2])
        return result

    def __conv_with_pattern(self, reading, morphs):
        if self.text_proc_index > 1:
            return reading, morphs

        conv_patterns = [
            ['ー', ''],
            ['ッ', ''],
            ['ン', ''],
            ['イウ', 'ユー'],
        ]
        for ptrn in conv_patterns:
            if ptrn[0] in reading:
                reading = reading.replace(ptrn[0], ptrn[1])
                morphs = [mrph.replace(ptrn[0], ptrn[1]) for mrph in morphs]
        return reading, morphs

    def __conv_vowel_to_pron(self, reading, morphs):
        conv_petterns = [
            ['オウ', lambda ch: ch[0] + 'ー'],
            ['エイ', lambda ch: ch[0] + 'ー'],
        ]

        for ptrn in conv_petterns:
            for ch in text_util.n_gram(reading, 2):
                if pyboin.text2boin(ch[0]) + ch[1] == ptrn[0]:
                    reading = reading.replace(ch, ptrn[1](ch))
                    morphs = [mrph.replace(ch, ptrn[1](ch)) for mrph in morphs]
        return reading, morphs

    def __conv_looped_vowel_to_hyphen(self, reading, morphs):
        reading = reading
        for i in range(len(reading) - 1):
            if reading[i + 1] not in 'アイウエオ':
                continue
            if pyboin.text2boin(reading[i]) == \
                    pyboin.text2boin(reading[i + 1]):
                reading = reading[:i + 1] + 'ー' + reading[i + 2:]
        reading = re.sub(r'ー+', 'ー', reading)
        return reading, morphs

    def __conv_prev_of_lower_ch_to_vowel(self, reading, morphs):
        for ch in re.findall(r'.[ァィゥェォャュョヮ]', reading):
            reading = reading.replace(
                ch,
                pyboin.convert_vowel(ch[0], pyboin.text2boin(ch[1]))
            )
        return reading, morphs

    def __rule_morphs_overlap(self, reading, morphs, is_tight=False):
        if is_tight:
            return False

        for mrp in morphs:
            if len(mrp) < 2:
                continue
            if self.ori_reading.count(mrp) >= 2:
                return True
        return False

    def __rule_full_match(self, reading, morphs, is_tight=False):
        ch_pair = self.__text_to_char_pair(reading)
        for ch1, ch2 in ch_pair:
            if self.__count_char_matches(ch1, ch2) == 3:
                for morph in morphs:
                    if self.__count_char_matches(ch1, morph, True) > 2:
                        return True
        return False

    def __rule_vowel_match(self, reading, morphs, is_tight=False):
        if is_tight:
            return False

        for ch1, ch2 in self.__text_to_char_pair(reading, 3):
            if self.__count_char_matches(ch1, ch2) < 2:
                continue
            if self.__count_char_matches(ch1, ch2, True) < 2:
                continue
            if sorted(pyboin.text2boin(ch1)) == sorted(pyboin.text2boin(ch2)):
                return True
        return False

    def __rule_consonant_match(self, reading, morphs, is_tight=False):
        if is_tight:
            return False

        for ch1, ch2 in self.__text_to_char_pair(reading, 3):
            if self.__count_char_matches(ch1, ch2) < 2:
                continue
            if self.__count_char_matches(ch1, ch2, True) < 2:
                continue
            if sorted([pyboin.convert_vowel(ch, 'ア') for ch in ch1]) == \
                    sorted([pyboin.convert_vowel(ch, 'ア') for ch in ch2]):
                return True
        return False

    def __rule_swap_match(self, reading, morphs, is_tight=False):
        if is_tight:
            return False

        for ch1, ch2 in self.__text_to_char_pair(reading, 3):
            if self.__count_char_matches(ch1, ch2) == 0:
                continue
            if self.__count_char_matches(ch1, ch2, no_order=True) == 3:
                return True

        return False

    def __rule_magic_nn(self, reading, morphs, is_tight=False):
        if is_tight:
            return False

        for ch1, ch2 in self.__text_to_char_pair(reading, 3):
            if self.__count_char_matches(ch1, ch2, magic_nn=True) == 3:
                return True

        return False

    def __reject_force_patterns(self, text):
        for ptrn in self.reject_patterns:
            if re.search(ptrn, text) is not None:
                return True

    def __reject_only_katakana(self, text):
        return re.fullmatch(r'[ァ-ヴー]+', text)

    def __reject_length(self, text):
        return len(text) >= 30

    def __reject_ch_many_times_used(self, text):
        cnt_ch = collections.Counter(text).most_common()
        if cnt_ch != []:
            return cnt_ch[0][1] >= 6

    def __reject_only_used_alphanumeric(self, text):
        return re.fullmatch(r'[\da-zA-Z]*', text) is not None

    def __reject_block_many_times_used(self, text):
        chars = []
        chars.extend(re.findall(r'[ぁ-んー]{3,}', text))
        chars.extend(re.findall(r'[ァ-ンー]{3,}', text))
        return len(set(chars)) != len(chars)

    def __reject_2_ch_match(self, text):
        if self.__full_text_n_matches(self.ori_reading) >= 4:
            chars = re.findall(r'[^ぁ-んァ-ンー][^\da-zA-Z].{3}', text)
            return len(set(chars)) != len(chars)
        chars = re.findall(r'[^ぁ-んァ-ンー][^\da-zA-Z]', text)
        return len(set(chars)) != len(chars)

    def __reject_lapel_pattern(self, text):
        pivot = len(text) // 2
        return text[:pivot] == text[pivot + len(text) % 2:]

    def __reject_len_of_sentence_and_ch(self, text):
        ch_len_rules = [
            [3, 0],
            [4, 7],
            [5, 10],
        ]
        chars = [ch for ch in text]
        for rule in ch_len_rules:
            if len(set(chars)) <= rule[0] and len(text) >= rule[1]:
                return True

    def __full_text_n_matches(self, reading: str) -> int:
        result: int = 0
        for n in range(len(reading)):
            for ch1, ch2 in self.__text_to_char_pair(reading, n + 1):
                if self.__count_char_matches(ch1, ch2) == n + 1:
                    result = n
        return result

    def __count_char_matches(self, ch1: str, ch2: str, no_order: bool = False, magic_nn: bool = False):
        if len(ch1) != len(ch2):
            return 0

        result = 0
        for i in range(len(ch1)):
            if no_order:
                if ch1[i] in ch2:
                    ch2 = ch2.replace(ch1[i], '', 1)
                    result += 1
            else:
                if ch1[i] == ch2[i]:
                    result += 1
                elif magic_nn and (ch1[i] == 'ン' or ch2[i] == 'ン'):
                    magic_nn = False
                    result += 1

        return result
