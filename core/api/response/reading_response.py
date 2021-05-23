from pydantic import BaseModel


class ReadingResponse(BaseModel):
    reading: str
