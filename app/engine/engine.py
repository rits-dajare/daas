from functools import lru_cache


class Engine():
    def __init__(self):
        self._sub_init()

    def _sub_init(self):
        raise Exception('サブクラスの責務')

    @lru_cache(maxsize=255)
    def execute(self):
        raise Exception('サブクラスの責務')
