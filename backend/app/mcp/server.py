from mcp.server.mcpserver import MCPServer

from ..config import get_settings
from ..dependencies.book_dependencies import BOOK_ROUTE
from ..dependencies.embed_dependencies import get_embed_model
from ..services.book_service import BookService
from ..services.question_service import QuestionService

server = MCPServer("streber")


def _question_service() -> QuestionService:
    return QuestionService(settings=get_settings(), embed_model=get_embed_model())


def _book_service() -> BookService:
    return BookService(route=BOOK_ROUTE, settings=get_settings(), embed_model=get_embed_model())


@server.tool()
def search_books(question: str, top_k: int = 10) -> list[dict]:
    """Pretražuje knjige i vraća relevantne tekstualne ulomke sa izvorom (file_name) i skorom."""
    top_k = max(1, min(top_k, 50))
    chunks = _question_service().retrieve(question, top_k=top_k)
    return [
        {"text": chunk.text, "file_name": chunk.file_name, "score": chunk.score}
        for chunk in chunks
    ]


@server.tool()
def ask_question(question: str) -> str:
    """Postavlja pitanje nad knjigama i vraća LLM odgovor zasnovan na pronađenim ulomcima."""
    return _question_service().get_answers(question)


@server.tool()
def list_books() -> list[str]:
    """Vraća listu naziva knjiga dostupnih u folderu data/book."""
    return [b.name for b in _book_service().list_books()]
