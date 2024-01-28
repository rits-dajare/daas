from pydantic import BaseModel


class JudgeV1:
    class Request(BaseModel):
        dajare: str

    class Response(BaseModel):
        is_dajare: bool
        applied_rule: str
