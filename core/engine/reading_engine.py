from functools import lru_cache

from core import config
from core import preprocessing


class ReadingEngine:
    def __init__(self):
        self.score_cache: list = []

    @lru_cache(config.CACHE_SIZE)
    def exec(self, text: str) -> str:
        # preprocessing
        result: str = preprocessing.filtering(text)
        result = preprocessing.reading(result)

        return result
