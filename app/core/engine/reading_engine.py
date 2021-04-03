from functools import lru_cache

from core import config
from core import preprocessing


class ReadingEngine:
    def __init__(self):
        self.score_cache: list = []

    @lru_cache(config.CACHE_SIZE)
    def exec(self, text: str) -> float:
        # preprocessing
        text = preprocessing.filtering(text)
        text = preprocessing.reading(text)

        return text
