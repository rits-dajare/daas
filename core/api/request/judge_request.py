from pydantic import BaseModel


class JudgeRequest(BaseModel):
    dajare: str
