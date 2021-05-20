from core.util import text_util


class ReadingEngine:
    def __init__(self):
        self.score_cache: list = []

    def exec(self, text: str) -> str:
        # text_util
        result: str = text_util.filtering(text)
        result = text_util.reading(result)

        return result
