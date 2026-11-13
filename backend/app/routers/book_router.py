from fastapi import APIRouter, Depends
from ..dependencies.book_dependencies import get_book_service

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/")
def list_book_files(
    service=Depends(get_book_service),
):
    files = service.list_books()
    print([b for b in files])

    index = service.index_books(files)
    print(index)
    return {"Status": "Success"}
