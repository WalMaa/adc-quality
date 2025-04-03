import sys
import importlib.util
from pathlib import Path
from unittest.mock import patch, MagicMock

db_path = Path(__file__).resolve().parents[2] / "src" / "db.py"
spec = importlib.util.spec_from_file_location("db", db_path)
db = importlib.util.module_from_spec(spec)
sys.modules["db"] = db
spec.loader.exec_module(db)


@patch("db.MongoClient")
def test_init_db_success(mock_mongo_client):
    """
    Test that init_db() successfully initializes MongoDB client and database,
    calls the 'ping' command, and creates collections.
    """
    mock_client = MagicMock()
    mock_db = MagicMock()

    mock_mongo_client.return_value = mock_client
    mock_client.__getitem__.return_value = mock_db
    mock_db.list_collection_names.return_value = []

    client, db_obj = db.init_db()

    assert client == mock_client
    assert db_obj == mock_db
    mock_client.admin.command.assert_called_once_with("ping")
    assert mock_db.create_collection.call_count == 3


@patch("db.MongoClient", side_effect=Exception("Connection error"))
def test_init_db_failure(mock_mongo_client):
    """
    Test that init_db() handles MongoDB connection failure and returns (None, None).
    """
    client, db_obj = db.init_db()
    assert client is None
    assert db_obj is None


@patch.object(db, 'db')
def test_create_collections_creates_missing(mock_db):
    """
    Test that create_collections() creates collections that do not already exist.
    """
    mock_db.list_collection_names.return_value = ["user_messages"]

    db.create_collections()

    mock_db.create_collection.assert_any_call("system_messages")
    mock_db.create_collection.assert_any_call("responses")
    assert mock_db.create_collection.call_count == 2


@patch.object(db, 'db')
def test_create_collections_all_exist(mock_db):
    """
    Test that create_collections() does not create any collections if they already exist.
    """
    mock_db.list_collection_names.return_value = [
        "user_messages", "system_messages", "responses"
    ]

    db.create_collections()

    mock_db.create_collection.assert_not_called()


def test_get_database_returns_global_db():
    """
    Test that get_database() returns the global db object.
    """
    original_db = db.db
    try:
        mock_db = MagicMock()
        db.db = mock_db
        assert db.get_database() == mock_db
    finally:
        db.db = original_db
