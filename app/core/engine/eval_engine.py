import numpy as np
from functools import lru_cache

from core import config
from core import preprocessing


class EvalEngine:
    def __init__(self):
        self.score_cache: list = []

    @lru_cache(config.CACHE_SIZE)
    def exec(self, text: str) -> float:
        # preprocessing
        text = preprocessing.filtering(text)
        text = preprocessing.reading(text)

        # check fuzzy cache
        for cache in self.score_cache:
            if cache['text'] in text or text in cache['text']:
                return cache['score']

        # score
        reading: str = preprocessing.reading(text)
        vector: list = preprocessing.vectorize(reading)
        result = self.eval(vector)

        # store fuzzy cache
        cache_data: dict = {'text': text, 'score': result}
        if len(self.score_cache) >= config.CACHE_SIZE:
            self.score_cache.pop(0)
            self.score_cache[-1] = cache_data
        else:
            self.score_cache.append(cache_data)

        return result

    def eval(self, vector: str) -> float:
        np.random.seed(sum(vector))
        result = np.random.normal(2, 1.3) + 1.0
        if result > 5.0:
            return 5.0 - np.random.rand() / 5
        if result < 1.0:
            return 1.0 + np.random.rand() / 5

        return result
