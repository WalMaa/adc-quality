from unittest.mock import patch, MagicMock
from backend.src import repository


@patch("backend.src.repository.MongoClient")
def test_init_db_sets_client_db_and_collection(mock_mongo_client):
    """
    Test that init_db sets the global client, db, and batches_collection.
    """
    mock_client = MagicMock()
    mock_db = MagicMock()
    mock_collection = MagicMock()

    mock_mongo_client.return_value = mock_client
    mock_client.__getitem__.return_value = mock_db
    mock_db.__getitem__.return_value = mock_collection

    repository.init_db()

    mock_mongo_client.assert_called_once_with("mongodb://localhost:27017")
    mock_client.__getitem__.assert_called_with("llm_dispatch")
    mock_db.__getitem__.assert_called_with("message_batches")

    assert repository.client == mock_client
    assert repository.db == mock_db
    assert repository.batches_collection == mock_collection
