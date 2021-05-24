from core.util import text_util


class ReadingEngine:
    def exec(self, text: str) -> str:
        # text_util
        result: str = text_util.preprocessing(text)
        result = text_util.reading(result)

        return result
