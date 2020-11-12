class Engine():
    def __init__(self):
        from .text.text_service import TextService
        self.__text_service = TextService()

        self._sub_init()

    def _sub_init(self):
        raise Exception('サブクラスの責務')

    def execute(self):
        raise Exception('サブクラスの責務')

    @property
    def text_service(self):
        return self.__text_service
