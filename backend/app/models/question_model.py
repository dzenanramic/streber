from pydantic import BaseModel


class QuestionModel(BaseModel):
    text: str
