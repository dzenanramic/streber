from pydantic import BaseModel


class QuestionModel(BaseModel):
    text: str


class RetrievedChunk(BaseModel):
    text: str
    file_name: str | None = None
    score: float | None = None
    metadata: dict | None = None
