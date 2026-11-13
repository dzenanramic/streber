from pathlib import Path
from fastapi import Depends
from ..config import Settings, get_settings
from ..services.book_service import BookService
from .embed_dependencies import get_embed_model

ROOT_ROUTE = Path(__file__).resolve().parents[2]
BOOK_ROUTE = ROOT_ROUTE / "data/book"


def get_book_service(
    embed_model=Depends(get_embed_model),
    settings: Settings = Depends(get_settings),
):
    return BookService(route=BOOK_ROUTE, settings=settings, embed_model=embed_model)
