# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------
import sys
from pathlib import Path
sys.path.append(str(Path('__file__').resolve().parent))
# --------------------------------------------------------------------------------------
from webapi import docomo
import webapi
# --------------------------------------------------------------------------------------


class Engine():
    def to_reading(self, dajare):
        res = webapi.docomo.to_reading(dajare)
        body = res.json()

        if 'converted' in body:
            return body['converted'].replace(' ', '')

        return ''

    def find_sensitive_tags(self, dajare):
        res = webapi.docomo.find_sensitive_tags(dajare)
        body = res.json()

        if 'quotients' in body:
            return [tag['cluster_name'] for tag in body['quotients']]

        return []

