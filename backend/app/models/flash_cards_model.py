from ..database import Base
from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column


class FlashCard(Base):
    __tablename__ = "flashcards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject: Mapped[str] = mapped_column(String)
    question: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String, nullable=True)
    options: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    correct_answers: Mapped[int] = mapped_column(Integer, nullable=True)
    answers: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
