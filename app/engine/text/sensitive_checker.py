import re
import csv
from functools import lru_cache


class SensitiveChecker:
    def __init__(self):
        from .docomo_service import DocomoService
        self.__docomo_service = DocomoService()

        self.sensitive_patterns = self.__load_patterns()

    @lru_cache(maxsize=255)
    def execute(self, text, use_api=True):
        result = []

        if use_api and self.token_valid:
            result.extend(self.__docomo_service.sensitive_check(text))

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
        with open('conf/sensitive_patterns.csv') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row == []:
                    continue
                result.append(row)

        return result

    @property
    def token_valid(self):
        return self.__docomo_service.is_valid
