from fastapi import APIRouter, Depends
from ..dependencies.book_dependencies import get_book_service
from ..logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/")
def list_book_files(
    service=Depends(get_book_service),
):
    files = service.list_books()
    logger.info("Indexing %d book file(s): %s", len(files), [b.name for b in files])

    index = service.index_books(files)
    logger.info("Index built: %s", index)
    return {"Status": "Success"}
