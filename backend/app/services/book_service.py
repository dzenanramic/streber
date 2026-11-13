from pathlib import Path
import pymupdf4llm
from ..repository.book_repository import BookRepository
from llama_index.core import Document
from unstructured.partition.docx import partition_docx


class BookService:
    def __init__(self, route, settings, embed_model):
        self.route = route
        self.embed_model = embed_model
        self.vector_repository = BookRepository(
            settings=settings, embed_model=embed_model
        )

    def list_books(self):
        books = [b for b in self.route.iterdir() if b.is_file()]
        return books

    def parse_books(self, books: list[Path]):
        documents = []
        for b in books:
            suffix = b.suffix.lower()

            if suffix == ".pdf":
                text = pymupdf4llm.to_markdown(str(b))

            elif suffix in [".docx", ".doc"]:
                elements = partition_docx(filename=str(b))
                text = "\n\n".join([str(element) for element in elements])

            else:
                continue

            doc = Document(
                text=text, metadata={"file_name": b.name, "file_path": str(b)}
            )
            documents.append(doc)

        return documents

    def index_books(self, books: list[Path]):
        documents = self.parse_books(books)
        return self.vector_repository.create_index(documents)
