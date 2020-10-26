from .judge_engine import JudgeEngine
from .eval_engine import EvalEngine
from .text.katakanizer import Katakanizer
from .text.sensitive_checker import SensitiveChecker


katakanizer = Katakanizer()
sensitive_checker = SensitiveChecker()
judge_engine = JudgeEngine(katakanizer)
eval_engine = EvalEngine(katakanizer)
