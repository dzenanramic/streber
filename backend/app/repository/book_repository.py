from llama_index.core import Document, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.postgres import PGVectorStore
from ..config import Settings


class BookRepository:
    def __init__(self, settings: Settings, embed_model):
        self.settings = settings
        self.embed_model = embed_model

    def _get_vector_store(self):
        s = self.settings

        return PGVectorStore.from_params(
            host=s.postgres_host,
            database=s.postgres_db,
            user=s.postgres_user,
            password=s.postgres_password,
            table_name=s.book_table_name,
            port=s.postgres_port,
            embed_dim=s.embedding_dim,
        )

    def create_index(self, documents: list[Document]) -> VectorStoreIndex:
        vector_store = self._get_vector_store()
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=200)

        return VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            transformations=[splitter],
            embed_model=self.embed_model,
        )
