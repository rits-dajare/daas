alphabets = {
    'a': 'エー',
    'b': 'ビー',
    'c': 'シー',
    'd': 'ディー',
    'e': 'イー',
    'f': 'エフ',
    'g': 'ジー',
    'h':  'エッチ',
    'i': 'アイ',
    'j': 'ジェー',
    'k': 'ケー',
    'l': 'エル',
    'm': 'エム',
    'n': 'エヌ',
    'o': 'オー',
    'p': 'ピー',
    'q': 'キュー',
    'r': 'アール',
    's': 'エス',
    't': 'ティー',
    'u': 'ユー',
    'v': 'ブイ',
    'w': 'ダブリュ',
    'x': 'エックス',
    'y': 'ワイ',
    'z': 'ゼット',
}


def convert_word_to_alphabet(text):
    alphabet_text = ''

    for ch in text:
        if ch in alphabets:
            alphabet_text += alphabets[ch]

    return alphabet_text
