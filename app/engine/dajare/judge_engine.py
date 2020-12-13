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
        self.reject_patterns = self.__load_patterns(
            'config/reject_patterns.txt')

    @lru_cache(maxsize=255)
    def execute(self, text, use_api=True):
        text = self.__text_service.cleaned(text)

        # ダジャレとみなす
        if self.__force_pass(text):
            return True
        # ダジャレとみなさない
        if self.__force_reject(text):
            return False

        katakana = self.__text_service.katakanize(text, use_api)
        katakana = self.__text_service.normalize(katakana)
        if text == 'あいうあいう-ん':
            print(katakana)
        morphs = self.__text_service.morphs(text)
        morphs = [self.__text_service.normalize(m) for m in morphs]

        return self.__rec_judge(katakana, morphs, len(katakana) >= 20)

    def __judge(self, katakana, morphs, is_tight=False):
        methods = [
            # 2文字以上の形態素が一致
            self.__rule_morphs_overlap,
            # 3文字完全一致
            self.__rule_full_match,
            # 3文字順不同一致
            self.__rule_match_no_order,
            # 2文字完全一致 & 母音完全一致
            self.__rule_vowel_match,
            # 2文字完全一致 & 子音完全一致
            self.__rule_consonant_match,
        ]

        for method in methods:
            if method(katakana, morphs, is_tight):
                return True

        return False

    def __rec_judge(self, katakana, morphs, is_tight=False):
        if self.__judge(katakana, morphs, is_tight):
            return True
        if is_tight:
            return False

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
            conv_katakana, conv_morphs = method(katakana, morphs)
            if conv_katakana != katakana:
                if self.__rec_judge(conv_katakana, conv_morphs, is_tight):
                    return True

        return False

    def __force_pass(self, text):
        for pattern in self.pass_patterns:
            if re.search(pattern, text) is not None:
                return True

        return False

    def __force_reject(self, text):
        methods = [
            # 強制的に弾くパターン
            self.__reject_force_patterns,
            # 30文字以上
            self.__reject_length,
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
                return True

        return False

    def __load_patterns(self, file):
        result = []
        with open(file, 'r') as f:
            result = f.read().split('\n')
            result.remove('')

        return result

    def __text_to_char_pair(self, katakana, n=3):
        result = []
        n_gram = self.__text_service.n_gram(katakana, n)
        for i, ch1 in enumerate(n_gram):
            for ch2 in n_gram[i + 1:]:
                result.append([ch1, ch2])
        return result

    def __conv_with_pattern(self, katakana, morphs):
        conv_patterns = [
            ['ー', ''],
            ['ッ', ''],
            ['ン', ''],
            ['イウ', 'ユー'],
        ]
        for ptrn in conv_patterns:
            if ptrn[0] in katakana:
                katakana = katakana.replace(ptrn[0], ptrn[1])
                morphs = [mrph.replace(ptrn[0], ptrn[1]) for mrph in morphs]
        return katakana, morphs

    def __conv_vowel_to_pron(self, katakana, morphs):
        conv_petterns = [
            ['オウ', lambda ch: ch[0] + 'ー'],
            ['エイ', lambda ch: ch[0] + 'ー'],
        ]

        for ptrn in conv_petterns:
            for ch in self.__text_service.n_gram(katakana, 2):
                if pyboin.text2boin(ch[0]) + ch[1] == ptrn[0]:
                    katakana = katakana.replace(ch, ptrn[1](ch))
                    morphs = [mrph.replace(ch, ptrn[1](ch)) for mrph in morphs]
        return katakana, morphs

    def __conv_looped_vowel_to_hyphen(self, katakana, morphs):
        katakana = katakana
        for i in range(len(katakana) - 1):
            if katakana[i + 1] not in 'アイウエオ':
                continue
            if pyboin.text2boin(katakana[i]) == \
                    pyboin.text2boin(katakana[i + 1]):
                katakana = katakana[:i + 1] + 'ー' + katakana[i + 2:]
        katakana = re.sub(r'ー+', 'ー', katakana)
        return katakana, morphs

    def __conv_prev_of_lower_ch_to_vowel(self, katakana, morphs):
        for ch in re.findall(r'.[ァィゥェォャュョヮ]', katakana):
            katakana = katakana.replace(
                ch,
                pyboin.romanize(ch[0], pyboin.text2boin(ch[1]))
            )
        return katakana, morphs

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

    def __reject_force_patterns(self, text):
        for ptrn in self.reject_patterns:
            if re.search(ptrn, text) is not None:
                return True

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
        chars = re.findall(r'[^ぁ-んァ-ン][^\da-zA-Z]', text)
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
