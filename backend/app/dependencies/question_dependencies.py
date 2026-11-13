from ..services.question_service import QuestionService
from fastapi import Depends
from ..config import get_settings
from .embed_dependencies import get_embed_model


def get_question_service(
    settings=Depends(get_settings),
    embed_model=Depends(get_embed_model),
):
    return QuestionService(
        settings=settings,
        embed_model=embed_model,
    )
