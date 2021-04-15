import re
import csv
import emoji
import pyboin
import jaconv
from janome.tokenizer import Tokenizer

from core import config


# morph analyzer
tokenizer = Tokenizer()


def reading(text: str) -> str:
    result: str = text

    # convert with dict
    with open(config.READING_DICT_FILE_PATH, 'r') as f:
        reader = csv.reader(f)
        for pattern in reader:
            if pattern != []:
                result = re.sub(*pattern, result)

    # convert with morph analysis
    result: str = ''.join(convert_morphs(result))

    # words that cannot be converted
    result = re.sub(r'[a-zA-Z][a-z]+', '', result)
    for word in re.findall(r'[a-zA-Z]+', result):
        result = result.replace(
            word,
            pyboin.alphabet_to_reading(word)
        )

    return result


def convert_morphs(text: str, filtering: bool = False) -> str:
    result: list = []
    filter_parts: list = ['助詞', '助動詞']

    for token in tokenizer.tokenize(text):
        for part in filter_parts:
            if filtering and part in token.part_of_speech:
                break
        else:
            if token.reading == '*':
                result.append(jaconv.hira2kata(token.surface))
            else:
                result.append(token.reading)

    return result


def filtering(text: str) -> str:
    result: str = text
    # remove symbolic char
    result = re.sub(r'[\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7E]', '', result)
    result = re.sub(r'[！-／：-＠［-｀｛-～、-〜”’・]', '', result)
    # remove emoji
    result = ''.join(ch for ch in result if ch not in emoji.UNICODE_EMOJI['en'])
    # remove '笑'
    result = re.sub(r'w+(?![a-vx-zA-Z])', '', result)
    # remove number
    result = re.sub(r'\d', '', result)

    return result


def n_gram(text: str, n: int = 3) -> list:
    return [text[idx:idx + n] for idx in range(len(text) - n + 1)]


def normalize(text: str) -> str:
    result: str = text

    # sub table
    sub_table: list = [
        'ヲヂガギグゲゴザジズゼゾダヂヅデドバビブヴベボパピプペポ〜',
        'オジカキクケコサシスセソタチツテトハヒフフヘホハヒフヘホー'
    ]
    for i in range(len(sub_table[0])):
        result = result.replace(
            sub_table[0][i],
            sub_table[1][i],
        )

    # squash chars that loop 3~ times
    result = re.sub(r'(.)\1{2,}', r'\1', result)

    return result


def vectorize(text: str) -> list:
    result: list = list(map(ord, text))
    # trimming
    result = result[:config.TEXT_MAX_LENGTH]
    # padding
    result += [0] * (config.TEXT_MAX_LENGTH - len(result))

    return result
