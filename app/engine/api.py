from .judge_engine import JudgeEngine
from .eval_engine import EvalEngine
from .text.reading.reading_service import ReadingService
from .text.sensitive.checker import SensitiveChecker


reading_converter = ReadingService()
sensitive_checker = SensitiveChecker()
judge_engine = JudgeEngine(reading_converter)
eval_engine = EvalEngine(reading_converter)
