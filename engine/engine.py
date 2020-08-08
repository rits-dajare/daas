# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------
import sys
from pathlib import Path
sys.path.append(str(Path('__file__').resolve().parent))
# --------------------------------------------------------------------------------------
import re
import csv
import webapi
from engine import alphabet
# --------------------------------------------------------------------------------------


class Engine():
    def __init__(self, reading_converter):
        self.reading_converter = reading_converter

        # force judge as dajare
        self.force_judge_pattern = open('config/force_judge_pattern.txt').read()
        self.force_judge_pattern = self.force_judge_pattern.split('\n')
        self.force_judge_pattern.remove('')

        # force add sensitive tag
        self.force_sensitive_pattern = []
        with open('config/force_sensitive_pattern.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if row != []:
                    self.force_sensitive_pattern.append(row)

        self._setup()

    def _setup(self):
        raise Exception('サブクラスの責務')

    def exclude_noise(self, text):
        noise = re.compile(r'[^0-9A-Za-z\u3041-\u3096\u30A1-\u30F6\u3005-\u3006\u3400-\u3fff\u2E80-\u2FDF\u3005-\u3007\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\U00020000-\U0002EBEFー]')
        return noise.sub('', text)

    def to_reading(self, dajare):
        dajare = self.exclude_noise(dajare)

        # exclude tail's 'w'
        noise = re.compile(r'w+$')
        if re.search(r'[a-vx-zA-VX-Z]w+$', dajare) is None:
            dajare = noise.sub('', dajare)

        reading = self.reading_converter.convert(dajare)

        words = re.findall(r'[a-zA-Z]{4,}', dajare)
        for w in words:
            reading = reading.replace(alphabet.convert_word_to_alphabet(w.lower()), '')

        return reading

    def find_sensitive_tags(self, dajare):
        res = webapi.docomo.find_sensitive_tags(dajare)
        body = res.json()

        sensitive_tags = []

        if 'quotients' in body:
            sensitive_tags = [tag['cluster_name'] for tag in body['quotients']]

        # force add sensitive tag
        for pattern in self.force_sensitive_pattern:
            if re.search(pattern[0], dajare) is not None:
                sensitive_tags.append(pattern[1])

        return list(set(sensitive_tags))

