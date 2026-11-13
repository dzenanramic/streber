from pathlib import Path
from fastapi import Depends
from ..config import Settings, get_settings
from ..services.book_service import BookService
from ..services.flash_card_service import FlashCardService
from .embed_dependencies import get_embed_model

ROOT_ROUTE = Path(__file__).resolve().parents[2]
BOOK_ROUTE = ROOT_ROUTE / "data/flash_cards"


def get_flash_card_services(
    settings: Settings = Depends(get_settings),
    embed_model=Depends(get_embed_model),
):
    book_service = BookService(
        route=BOOK_ROUTE, settings=settings, embed_model=embed_model
    )
    flash_card_service = FlashCardService(settings=settings, embed_model=embed_model)

    return book_service, flash_card_service
