import csv
import re
from .text_engine import TextEngine


class SensitiveChecker(TextEngine):
    def _sub_init(self):
        self.sensitive_patterns = self.__load_patterns()

    def check(self, text, use_api=True):
        result = []

        if use_api and self.token_valid:
            body = self._call_api(
                'https://api.apigw.smt.docomo.ne.jp/truetext/v1/sensitivecheck',
                {'Content-Type': 'application/x-www-form-urlencoded'},
                {'text': text},
            )
            result.extend(self.__extract_tags_from_res(body))

        result.extend(self.__force_tagging(text))
        result = list(set(result))
        result.sort()

        return result

    def __force_tagging(self, text):
        result = []
        for pattern in self.sensitive_patterns:
            if re.search(pattern[0], text) is None:
                continue
            result.append(pattern[1])

        return result

    def __load_patterns(self):
        result = []
        with open('config/sensitive_patterns.csv') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row == []:
                    continue
                result.append(row)

        return result

    def __extract_tags_from_res(self, body):
        result = []

        if body is None:
            return result
        if 'quotients' not in body:
            return result

        for word_tags in body['quotients']:
            for tag in word_tags['cluster_name'].split('・'):
                if ':' in tag:
                    continue
                result.append(tag)

        return result
