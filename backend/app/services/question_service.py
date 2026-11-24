from ..config import Settings
from ..repository.book_repository import BookRepository
from llama_index.core import VectorStoreIndex
from ..clients.deepseek_client import get_response
from ..models.question_model import RetrievedChunk


class QuestionService:
    def __init__(self, settings: Settings, embed_model):
        self.settings = settings
        self.embed_model = embed_model
        self.vector_repository = BookRepository(
            settings=settings, embed_model=embed_model
        )

    def retrieve(self, question: str, top_k: int = 10) -> list[RetrievedChunk]:
        vector_store = self.vector_repository._get_vector_store()
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store, embed_model=self.embed_model
        )
        retriever = index.as_retriever(similarity_top_k=top_k)

        nodes = retriever.retrieve(question)
        chunks = []
        for node_with_score in nodes:
            node = node_with_score.node
            chunks.append(
                RetrievedChunk(
                    text=node.get_content(),
                    file_name=node.metadata.get("file_name"),
                    score=node_with_score.score,
                    metadata=node.metadata,
                )
            )
        return chunks

    def get_answers(self, question, top_k: int = 10):
        chunks = self.retrieve(question, top_k=top_k)

        content = []
        for i, chunk in enumerate(chunks, start=1):
            content.append(f'<doc id="{i} metadata ={chunk.metadata}">\n{chunk.text}\n</doc>')

        context_str = "\n\n".join(content)
        ai_response = get_response(context=context_str, question=question)
        return ai_response
