from fastapi import APIRouter, Depends
from ..models.question_model import QuestionModel
from ..dependencies.question_dependencies import get_question_service

router = APIRouter(prefix="/question", tags=["question"])


@router.post("/")
def get_answer(payload: QuestionModel, answer=Depends(get_question_service)):
    answers = answer.get_answers(payload.text)
    # print(answers)
    return answers
