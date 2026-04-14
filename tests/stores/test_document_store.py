from src.stores.document_store import DocumentStore


def test_save_and_get_annotation(tmp_path):
    filepath = tmp_path / "documents.json"
    store = DocumentStore(filepath=str(filepath))

    doc = {
        "image_id": "img_001",
        "image_path": "images/dog.jpg",
        "tags": [{"label": "dog", "score": 0.9}],
        "model_name": "test-model",
        "status": "stored",
    }

    store.save_annotation("img_001", doc)

    assert store.has_image("img_001") is True
    assert store.get_annotation("img_001") == doc


def test_empty_document_store(tmp_path):
    filepath = tmp_path / "documents.json"
    store = DocumentStore(filepath=str(filepath))

    assert store.has_image("img_001") is False
    assert store.get_annotation("img_001") is None
