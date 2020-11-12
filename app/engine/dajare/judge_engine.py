import re
from functools import lru_cache
import pyboin
import collections
from .. import engine


class JudgeEngine(engine.Engine):
    def _sub_init(self):
        from ..text.text_service import TextService
        self.__text_service = TextService()

        self.pass_patterns = self.__load_patterns('config/pass_patterns.txt')
        self.not_pass_patterns = self.__load_patterns(
            'config/not_pass_patterns.txt')

    @lru_cache(maxsize=255)
    def execute(self, text, use_api=True):
        # ダジャレとみなす
        if self.__force_pass(text):
            return True
        # ダジャレとみなさない
        if self.__force_not_pass(text):
            return False

        katakana = self.__text_service.katakanize(text, use_api)
        katakana = self.__text_service.normalize(katakana)
        morphs = self.__text_service.morphs(text)
        morphs = [self.__text_service.normalize(m) for m in morphs]

        return self.__rec_judge(katakana, morphs, len(katakana) >= 20)

    def __judge(self, katakana, morphs, is_tight=False):
        # 2文字以上の形態素が一致
        if self.__rule_morphs_overlap(katakana, morphs, is_tight):
            return True
        # 3文字完全一致
        if self.__rule_full_match(katakana, morphs, is_tight):
            return True
        # 3文字順不同一致
        if self.__rule_match_no_order(katakana, morphs, is_tight):
            return True
        # 2文字完全一致 & 母音完全一致
        if self.__rule_vowel_match(katakana, morphs, is_tight):
            return True
        # 2文字完全一致 & 子音完全一致
        if self.__rule_consonant_match(katakana, morphs, is_tight):
            return True

    def __rule_morphs_overlap(self, katakana, morphs, is_tight=False):
        for mrp in morphs:
            if len(mrp) < 2:
                continue
            if katakana.count(mrp) >= 2:
                return True
        return False

    def __rule_full_match(self, katakana, morphs, is_tight=False):
        ch_pair = self.__text_to_char_pair(katakana)
        for ch1, ch2 in ch_pair:
            if self.__text_service.count_char_matches(ch1, ch2) == 3:
                return True
        return False

    def __rule_match_no_order(self, katakana, morphs, is_tight=False):
        if is_tight:
            return False

        ch_pair = self.__text_to_char_pair(katakana)
        for ch1, ch2 in ch_pair:
            if sorted(ch1) == sorted(ch2):
                return True
        return False

    def __rule_vowel_match(self, katakana, morphs, is_tight=False):
        if is_tight:
            return False

        ch_pair = self.__text_to_char_pair(katakana)
        ch_pair.extend(self.__text_to_char_pair(katakana, 4))
        for ch1, ch2 in ch_pair:
            if self.__text_service.count_char_matches(ch1, ch2) < 2:
                continue
            if sorted(pyboin.text2boin(ch1)) == sorted(pyboin.text2boin(ch2)):
                return True
        return False

    def __rule_consonant_match(self, katakana, morphs, is_tight=False):
        if is_tight:
            return False

        ch_pair = self.__text_to_char_pair(katakana)
        ch_pair.extend(self.__text_to_char_pair(katakana, 4))
        for ch1, ch2 in ch_pair:
            if self.__text_service.count_char_matches(ch1, ch2) < 2:
                continue
            if sorted([pyboin.romanize(ch, 'ア') for ch in ch1]) == \
                    sorted([pyboin.romanize(ch, 'ア') for ch in ch2]):
                return True
        return False

    def __text_to_char_pair(self, katakana, n=3):
        result = []
        n_gram = self.__text_service.n_gram(katakana, n)
        for i, ch1 in enumerate(n_gram):
            for ch2 in n_gram[i + 1:]:
                result.append([ch1, ch2])
        return result

    def __rec_judge(self, katakana, morphs, is_tight=False):
        if self.__judge(katakana, morphs, is_tight):
            return True
        if is_tight:
            return False

        # パターンが含まれている場合，置換して再判定
        replace_patterns = [
            ['ー', ''],
            ['ッ', ''],
            ['ン', ''],
            ['イウ', 'ユー'],
        ]
        for pattern in replace_patterns:
            if pattern[0] in katakana:
                if self.__rec_judge(
                        katakana.replace(pattern[0], pattern[1]),
                        [m.replace(pattern[0], pattern[1]) for m in morphs],
                        is_tight):
                    return True

        # 母音を発音に変換
        vowel_patterns = [
            ['オウ', lambda ch: ch[0] + 'ー'],
            ['エイ', lambda ch: ch[0] + 'ー'],
        ]
        converted_katakana = katakana
        converted_morphs = morphs
        for bi_char in self.__text_service.n_gram(katakana, 2):
            for sub in vowel_patterns:
                if pyboin.text2boin(bi_char[0]) + bi_char[1] == sub[0]:
                    converted_katakana = converted_katakana.replace(
                        bi_char, sub[1](bi_char))
                    converted_morphs = [
                        m.replace(bi_char, sub[1](bi_char)) for m in converted_morphs]
        if converted_katakana != katakana:
            if self.__rec_judge(converted_katakana, converted_morphs, is_tight):
                return True

        # 連続された母音の末尾をハイフンに変換
        converted_katakana = katakana
        for ci in range(len(katakana) - 1):
            if converted_katakana[ci + 1] not in 'アイウエオ':
                continue
            if pyboin.text2boin(converted_katakana[ci]) == \
                    pyboin.text2boin(converted_katakana[ci + 1]):
                converted_katakana = \
                    converted_katakana[:ci + 1] + 'ー' + \
                    converted_katakana[ci + 2:]
        converted_katakana = re.sub(r'ー+', 'ー', converted_katakana)
        if converted_katakana != katakana:
            if self.__rec_judge(converted_katakana, morphs, is_tight):
                return True

        # 小文字の直前文字を小文字の母音に変換
        # ex. 'シュン' -> 'スン'
        matches = re.findall(r'.[ァィゥェォャュョヮ]', katakana)
        if matches != []:
            lower_to_vowel_katakana = katakana
            for ch in matches:
                lower_to_vowel_katakana = lower_to_vowel_katakana.replace(
                    ch,
                    pyboin.romanize(ch[0], pyboin.text2boin(ch[1]))
                )
            if self.__rec_judge(lower_to_vowel_katakana, morphs, is_tight):
                return True

        return False

    def __force_pass(self, text):
        for pattern in self.pass_patterns:
            if re.search(pattern, text) is not None:
                return True

        return False

    def __force_not_pass(self, text):
        for pattern in self.not_pass_patterns:
            if re.search(pattern, text) is not None:
                return True

        text = self.__text_service.cleaned(text)

        # 30文字以上
        if len(text) >= 30:
            return True
        # 同じ文字が6回以上使われている
        cnt_ch = collections.Counter(text).most_common()
        if cnt_ch != []:
            if cnt_ch[0][1] >= 6:
                return True
        # 半角文字のみ
        if re.fullmatch(r'[\da-zA-Z]*', text) is not None:
            return True
        # 同じひらがな/カタカナのブロックが重複
        chars = []
        chars.extend(re.findall(r'[ぁ-んー]{3,}', text))
        chars.extend(re.findall(r'[ァ-ンー]{3,}', text))
        if len(set(chars)) != len(chars):
            return True
        # 同じ2文字が含まれている
        cols = re.findall(r'[^ぁ-んァ-ン][^\da-zA-Z]', text)
        if len(cols) != len(set(cols)):
            return True
        # ABCD|ABCDパターン
        pivot = len(text) // 2
        if text[:pivot] == text[pivot + len(text) % 2:]:
            return True
        # [x, y]：文字がx種類以下 && 文字列がy文字以上
        chars_length_rules = [
            [3, 0],
            [4, 7],
            [5, 10],
        ]
        chars = [ch for ch in text]
        for rule in chars_length_rules:
            if len(set(chars)) <= rule[0] and len(text) >= rule[1]:
                return True

        return False

    def __load_patterns(self, file):
        result = []
        with open(file, 'r') as f:
            result = f.read().split('\n')
            result.remove('')

        return result
