import re
import emoji

from core import config


def filtering(text: str) -> str:
    result: str = text
    # remove symbolic char
    result = re.sub(r'[\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7E]', '', result)
    result = re.sub(r'[！-／：-＠［-｀｛-～、-〜”’・]', '', result)
    # remove emoji
    result = ''.join(ch for ch in result if ch not in emoji.UNICODE_EMOJI)
    # remove '笑'
    result = re.sub(r'w+(?![a-vx-zA-Z])', '', result)

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