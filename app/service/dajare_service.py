from functools import lru_cache

from app import config
from app.model.dajare_model import DajareModel
from app.service.engine.judge_engine import JudgeEngine
from app.service.engine.eval_engine import EvalEngine
from app.service.engine.reading_engine import ReadingEngine


class DajareService:
    def __init__(self):
        # create core engines
        self.__judge_engine = JudgeEngine()
        self.__eval_engine = EvalEngine()
        self.__reading_engine = ReadingEngine()

    @lru_cache(config.CACHE_SIZE)
    def judge_dajare(self, dajare_text: str) -> DajareModel:
        result = DajareModel()
        result.text = dajare_text
        result.is_dajare = self.__judge_engine.exec(dajare_text)
        result.applied_rule = self.__judge_engine.applied_rule
        return result

    @lru_cache(config.CACHE_SIZE)
    def eval_dajare(self, dajare_text: str) -> DajareModel:
        result = DajareModel()
        result.text = dajare_text
        result.score = self.__eval_engine.exec(dajare_text)
        return result

    @lru_cache(config.CACHE_SIZE)
    def convert_reading(self, dajare_text: str) -> DajareModel:
        result = DajareModel()
        result.text = dajare_text
        result.reading = self.__reading_engine.exec(dajare_text)
        return result
