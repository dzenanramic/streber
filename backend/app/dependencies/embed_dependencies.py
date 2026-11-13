from llama_index.embeddings.openai import OpenAIEmbedding

from ..config import get_settings


def get_embed_model() -> OpenAIEmbedding:
    settings = get_settings()

    return OpenAIEmbedding(
        model="text-embedding-3-small",
        api_key=settings.open_api_key,
    )
