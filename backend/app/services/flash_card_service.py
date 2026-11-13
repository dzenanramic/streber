from ..config import Settings
from llama_index.core import Document
from pathlib import Path
from unstructured.partition.docx import partition_docx
import pymupdf4llm
from ..repository.book_repository import BookRepository
from llama_index.core import VectorStoreIndex
from ..clients.deepseek_client import get_flash_card_response
import json
from ..models.flash_cards_model import FlashCard


class FlashCardService:
    def __init__(self, settings: Settings, embed_model):
        self.settings = settings
        self.embed_model = embed_model
        self.vector_repository = BookRepository(
            settings=settings, embed_model=embed_model
        )

    def parse_flash_card_questions(self, flash_card_questions: Path):
        suffix = flash_card_questions.suffix.lower()
        documents = []
        text = None
        if suffix == ".pdf":
            text = pymupdf4llm.to_markdown(str(flash_card_questions))
            print("THIS IS TEXT FROM PDF", text)
        elif suffix in [".docx", ".doc"]:
            elements = partition_docx(filename=str(flash_card_questions))
            text = "\n\n".join([str(element) for element in elements])

        doc = Document(text=text)

        documents.append(doc)

        return documents

    def get_flash_card_answers(self, questions, top_k: int = 10):
        vector_store = self.vector_repository._get_vector_store()
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store, embed_model=self.embed_model
        )
        retriever = index.as_retriever(similarity_top_k=top_k)

        content = []
        question_response = get_flash_card_response(questions)
        data = json.loads(question_response)
        return [FlashCard(**item) for item in data]

    # for i, question in enumerate(questions, start=1):
    # nodes = retriever.retrieve(question)
    # content.append(nodes)
    # for i, result in enumerate(nodes, start=1):
    #     node = result.node
    #     text = node.get_content()
    #     print(f"\n{'=' * 60}")
    #     print(f"REZULTAT: {i}")
    #     print(f"NODE ID: {node.node_id}")
    #     print(f"SCORE: {result.score}")
    #     print(f"METADATA: {node.metadata}")
    #     print(f"TEKST:\n{text}")

    #     content.append(
    #         f'<doc id="{i} metadata ={node.metadata}">\n{text}\n</doc>'
    #     )
    # print(questions)
