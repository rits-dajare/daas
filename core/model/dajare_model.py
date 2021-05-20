class DajareModel:
    __text: str
    __score: float
    __reading: str

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str):
        if not isinstance(text, str):
            raise TypeError('invalid type')
        self.__text = text

    @property
    def score(self) -> float:
        return self.__score

    @score.setter
    def score(self, score: float):
        if not isinstance(score, float):
            raise TypeError('invalid type')
        if not (score >= 1.0 and score <= 5.0):
            raise ValueError('score must be 1~5')

        self.__score = score

    @property
    def reading(self) -> str:
        return self.__reading

    @reading.setter
    def reading(self, reading: str):
        if not isinstance(reading, str):
            raise TypeError('invalid type')
        self.__reading = reading
