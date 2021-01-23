class Engine():
    def __init__(self, text_service):
        self.__text_service = text_service
        self._sub_init()

    def _sub_init(self):
        raise Exception('サブクラスの責務')

    def execute(self):
        raise Exception('サブクラスの責務')

    @property
    def text_service(self):
        return self.__text_service
