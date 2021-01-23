from functools import lru_cache
from .engine import Engine


class ReadingEngine(Engine):
    def _sub_init(self):
        pass

    @lru_cache(maxsize=255)
    def execute(self, text, use_api=True):
        return self.text_service.katakanize(text, use_api)
