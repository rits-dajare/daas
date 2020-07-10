# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------
import sys
from pathlib import Path
sys.path.append(str(Path('__file__').resolve().parent))
# --------------------------------------------------------------------------------------
import re
import csv
from webapi import docomo
import webapi
# --------------------------------------------------------------------------------------


class Engine():
    def __init__(self):
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

    def to_reading(self, dajare):
        res = webapi.docomo.to_reading(dajare)
        body = res.json()

        if 'converted' in body:
            return body['converted'].replace(' ', '')

        return ''

    def find_sensitive_tags(self, dajare):
        res = webapi.docomo.find_sensitive_tags(dajare)
        body = res.json()

        sensitive_tags = []

        if 'quotients' in body:
            sensitive_tags = [tag['cluster_name'] for tag in body['quotients']]

        # force add sensitive tag
        for pattern in self.force_sensitive_pattern:
            if re.match(pattern[0], dajare) is not None:
                sensitive_tags.append(pattern[1])

        return sensitive_tags

