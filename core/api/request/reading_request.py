class ReadingRequest:
    dajare: str

    def __init__(self, params: dict):
        self.dajare = params["dajare"]
