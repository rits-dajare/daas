from core.model.dajare_model import DajareModel
from core.service.engine.judge_engine import JudgeEngine
from core.service.engine.eval_engine import EvalEngine
from core.service.engine.reading_engine import ReadingEngine


class DajareService:
    def __init__(self):
        # create core engines
        self.__judge_engine = JudgeEngine()
        self.__eval_engine = EvalEngine()
        self.__reading_engine = ReadingEngine()

    def judge_dajare(self, dajare_text: str) -> DajareModel:
        result = DajareModel()
        result.text = dajare_text
        result.is_dajare = self.__judge_engine.exec(dajare_text)
        result.applied_rule = self.__judge_engine.applied_rule
        return result

    def eval_dajare(self, dajare_text: str) -> DajareModel:
        result = DajareModel()
        result.text = dajare_text
        result.score = self.__eval_engine.exec(dajare_text)
        return result

    def convert_reading(self, dajare_text: str) -> DajareModel:
        result = DajareModel()
        result.text = dajare_text
        result.reading = self.__reading_engine.exec(dajare_text)
        return result
