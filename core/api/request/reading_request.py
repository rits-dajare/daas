from pydantic import BaseModel


class ReadingRequest(BaseModel):
    dajare: str
