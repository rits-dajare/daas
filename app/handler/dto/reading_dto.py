from pydantic import BaseModel


class ReadingV1:
    class Request(BaseModel):
        dajare: str

    class Response(BaseModel):
        reading: str
