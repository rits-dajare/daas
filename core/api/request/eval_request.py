from pydantic import BaseModel


class EvalRequest(BaseModel):
    dajare: str
