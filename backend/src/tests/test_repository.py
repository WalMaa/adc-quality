import sys
import importlib.util
from pathlib import Path
from unittest.mock import patch, MagicMock

repo_path = Path(__file__).resolve().parents[2] / "src" / "repository.py"
spec = importlib.util.spec_from_file_location("repository_module", repo_path)
repository_module = importlib.util.module_from_spec(spec)
sys.modules["repository_module"] = repository_module
spec.loader.exec_module(repository_module)


@patch("repository_module.MongoClient")
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

    repository_module.init_db()

    mock_mongo_client.assert_called_once_with("mongodb://localhost:27017")
    mock_client.__getitem__.assert_called_with("llm_dispatch")
    mock_db.__getitem__.assert_called_with("message_batches")

    assert repository_module.client == mock_client
    assert repository_module.db == mock_db
    assert repository_module.batches_collection == mock_collection
