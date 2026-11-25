from fastapi import APIRouter, Depends
from ..dependencies.flash_card_dependencies import get_flash_card_services
from ..services.flash_card_service import FlashCardService
from ..services.book_service import BookService
from ..database import get_db
from ..repository.flash_cards_repository import FlashCardsRepository
from ..logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/flash-cards", tags=["flash-cards"])


@router.post("/")
def list_flash_card_files(
    service: tuple[BookService, FlashCardService] = Depends(get_flash_card_services),
    db=Depends(get_db),
):
    flash_card_repository = FlashCardsRepository(db=db)
    book_service, flash_card_service = service
    question_files = book_service.list_books()

    questions = []

    for q in question_files:
        parsed_questions = flash_card_service.parse_flash_card_questions(q)
        card_questions = flash_card_service.get_flash_card_answers(parsed_questions)

        for question in card_questions:
            logger.info("Creating flash card: %s", question.subject)
            flash_card_repository.create_flash_card(question)

        questions.append(card_questions)
        logger.info("Created %d flash card(s)", len(card_questions))

    return {"Card questions status": "Created"}


@router.get("/")
def get_cards(
    subject,
    db=Depends(get_db),
):
    flash_card_repository = FlashCardsRepository(db=db)
    return flash_card_repository.list_flash_cards(subject=subject)
