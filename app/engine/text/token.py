class Token:
    def __init__(self, token, is_valid=True):
        self.__token = token
        self.__is_valid = is_valid

    def enable(self):
        self.__is_valid = True

    def disable(self):
        self.__is_valid = False

    @property
    def token(self):
        return self.__token

    @property
    def is_valid(self):
        return self.__is_valid
