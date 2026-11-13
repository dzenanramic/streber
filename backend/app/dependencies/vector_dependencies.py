from fastapi import Depends

from ..repository.book_repository import BookRepository
from ..config import get_settings
from .embed_dependencies import get_embed_model


def get_book_repository(
    settings=Depends(get_settings), embed_model=Depends(get_embed_model)
) -> BookRepository:
    return BookRepository(settings, embed_model=embed_model)
