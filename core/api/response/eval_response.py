from pydantic import BaseModel


class EvalResponse(BaseModel):
    score: float
