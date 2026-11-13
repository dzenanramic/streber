from ..config import Settings
from ..repository.book_repository import BookRepository
from llama_index.core import VectorStoreIndex
from ..clients.deepseek_client import get_response


class QuestionService:
    def __init__(self, settings: Settings, embed_model):
        self.settings = settings
        self.embed_model = embed_model
        self.vector_repository = BookRepository(
            settings=settings, embed_model=embed_model
        )

    def get_answers(self, question, top_k: int = 10):
        vector_store = self.vector_repository._get_vector_store()
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store, embed_model=self.embed_model
        )
        retriever = index.as_retriever(similarity_top_k=top_k)

        nodes = retriever.retrieve(question)
        content = []
        for i, result in enumerate(nodes, start=1):
            node = result.node
            text = node.get_content()

            print(f"\n{'=' * 60}")
            print(f"REZULTAT: {i}")
            print(f"NODE ID: {node.node_id}")
            print(f"SCORE: {result.score}")
            print(f"METADATA: {node.metadata}")
            print(f"TEKST:\n{text}")

            content.append(f'<doc id="{i} metadata ={node.metadata}">\n{text}\n</doc>')

        context_str = "\n\n".join(content)
        print("OVO JE KONTEKST", context_str)
        ai_response = get_response(context=context_str, question=question)
        print(ai_response)
        return ai_response
