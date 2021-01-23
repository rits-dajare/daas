from .eval_engine import EvalEngine
from .judge_engine import JudgeEngine
from .reading_engine import ReadingEngine
from .text.text_service import TextService

text_service = TextService()

eval_engine = EvalEngine(text_service)
judge_engine = JudgeEngine(text_service)
reading_engine = ReadingEngine(text_service)
