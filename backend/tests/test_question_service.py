"""Unit test za QuestionService.retrieve() — sve vanjske granice su mockovane,
pa test ne treba bazu, embed model ni mrežu."""

from unittest.mock import MagicMock, patch

from app.services.question_service import QuestionService


def _fake_node_with_score(text, file_name, score):
    node = MagicMock()
    node.get_content.return_value = text
    node.metadata = {"file_name": file_name}
    ns = MagicMock()
    ns.node = node
    ns.score = score
    return ns


def test_retrieve_maps_nodes_to_chunks_and_forwards_top_k():
    fake_nodes = [
        _fake_node_with_score("prvi tekst", "patologija1.pdf", 0.9),
        _fake_node_with_score("drugi tekst", "patologija2.pdf", 0.5),
    ]
    fake_retriever = MagicMock()
    fake_retriever.retrieve.return_value = fake_nodes

    fake_index = MagicMock()
    fake_index.as_retriever.return_value = fake_retriever

    with (
        patch("app.services.question_service.BookRepository") as mock_repo_cls,
        patch("app.services.question_service.VectorStoreIndex") as mock_index_cls,
    ):
        mock_repo_cls.return_value._get_vector_store.return_value = object()
        mock_index_cls.from_vector_store.return_value = fake_index

        service = QuestionService(settings=MagicMock(), embed_model=object())
        chunks = service.retrieve("sta je patologija?", top_k=5)

    fake_index.as_retriever.assert_called_once_with(similarity_top_k=5)
    fake_retriever.retrieve.assert_called_once_with("sta je patologija?")

    assert len(chunks) == 2
    assert chunks[0].text == "prvi tekst"
    assert chunks[0].file_name == "patologija1.pdf"
    assert chunks[0].score == 0.9
    assert chunks[0].metadata == {"file_name": "patologija1.pdf"}
    assert chunks[1].text == "drugi tekst"
    assert chunks[1].file_name == "patologija2.pdf"
    assert chunks[1].score == 0.5
