from src.stores.vector_store import VectorStore


def test_save_and_search_single_embedding(tmp_path):
    index_path = tmp_path / "faiss.index"
    ids_path = tmp_path / "vector_ids.json"

    store = VectorStore(
        dim=3,
        index_path=str(index_path),
        ids_path=str(ids_path),
    )

    store.save_embedding("img_001", [1.0, 0.0, 0.0])

    assert store.has_image("img_001") is True
    assert store.get_count() == 1

    results = store.search([1.0, 0.0, 0.0], top_k=1)

    assert len(results) == 1
    assert results[0][0] == "img_001"
    assert results[0][1] > 0.99


def test_search_ranks_closest_embedding_first(tmp_path):
    index_path = tmp_path / "faiss.index"
    ids_path = tmp_path / "vector_ids.json"

    store = VectorStore(
        dim=3,
        index_path=str(index_path),
        ids_path=str(ids_path),
    )

    store.save_embedding("img_dog", [1.0, 0.0, 0.0])
    store.save_embedding("img_cat", [0.0, 1.0, 0.0])

    results = store.search([0.0, 1.0, 0.0], top_k=2)

    assert len(results) == 2
    assert results[0][0] == "img_cat"
    assert results[1][0] == "img_dog"
    assert results[0][1] > results[1][1]


def test_search_empty_store_returns_empty_list(tmp_path):
    index_path = tmp_path / "faiss.index"
    ids_path = tmp_path / "vector_ids.json"

    store = VectorStore(
        dim=3,
        index_path=str(index_path),
        ids_path=str(ids_path),
    )

    results = store.search([1.0, 0.0, 0.0], top_k=3)

    assert results == []
