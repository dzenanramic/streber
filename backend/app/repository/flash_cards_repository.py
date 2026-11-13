from ..models import FlashCard
from sqlalchemy.orm import Session


class FlashCardsRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_flash_card(self, flash_card: FlashCard) -> FlashCard:
        flash_card_item = FlashCard(
            subject=flash_card.subject,
            question=flash_card.question,
            type=flash_card.type,
            options=flash_card.options,
            correct_answers=flash_card.correct_answers,
            answers=flash_card.answers,
        )

        self.db.add(flash_card_item)
        self.db.commit()
        self.db.refresh(flash_card_item)
        return flash_card_item

    def list_flash_cards(self, subject) -> list[FlashCard]:
        return (
            self.db.query(FlashCard)
            .filter(FlashCard.subject == subject)
            .limit(10)
            .all()
        )
