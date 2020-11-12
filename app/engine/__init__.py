from .dajare.judge_engine import JudgeEngine
from .dajare.eval_engine import EvalEngine
from .text.text_service import TextService
from .text.katakanizer import Katakanizer
from .text.sensitive_checker import SensitiveChecker

text_service = TextService()
katakanizer = Katakanizer()
sensitive_checker = SensitiveChecker()
judge_engine = JudgeEngine()
eval_engine = EvalEngine()
