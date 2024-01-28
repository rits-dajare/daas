from pydantic import BaseModel


class EvalV1:
    class Request(BaseModel):
        dajare: str

    class Response(BaseModel):
        score: float
