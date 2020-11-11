import re
from .katakanizer import Katakanizer


class TextService:
    def __init__(self):
        self.__katakanizer = Katakanizer()

    def katakanize(self, text):
        return self.__katakanizer.katakanize(text)
