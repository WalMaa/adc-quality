import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from bson import ObjectId
from backend.src.routes import messages

app = FastAPI()
app.include_router(messages.router)
client = TestClient(app)

FAKE_ID = str(ObjectId())


@pytest.fixture
def mock_db():
    with patch("backend.src.routes.messages.get_database") as mock_get_db:
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        yield mock_db


def test_save_user_message(mock_db):
    """
    Test saving a user message successfully.
    """
    mock_collection = MagicMock()
    mock_db.get_collection.return_value = mock_collection

    response = client.post("/messages/user", json={"message": "Hello!"})
    assert response.status_code == 200
    assert response.text == '"User message saved"'


def test_save_system_message(mock_db):
    """
    Test saving a system message successfully.
    """
    mock_collection = MagicMock()
    mock_collection.insert_one.return_value.inserted_id = FAKE_ID
    mock_db.get_collection.return_value = mock_collection

    response = client.post("/messages/system", json={"message": "System log"})
    assert response.status_code == 200
    assert response.text == '"System message saved"'


def test_list_user_messages(mock_db):
    """
    Test listing user messages with mocked documents.
    """
    mock_cursor = [{"_id": ObjectId(), "message": "User 1"}]
    mock_db.__getitem__.return_value.find.return_value = mock_cursor

    response = client.get("/messages/user")
    assert response.status_code == 200
    assert response.json()[0]["message"] == "User 1"
    assert "_id" in response.json()[0]


def test_list_system_messages(mock_db):
    """
    Test listing system messages with mocked documents.
    """
    mock_cursor = [{"_id": ObjectId(), "message": "System 1"}]
    mock_db.__getitem__.return_value.find.return_value = mock_cursor

    response = client.get("/messages/system")
    assert response.status_code == 200
    assert response.json()[0]["message"] == "System 1"


def test_get_user_message_found(mock_db):
    """
    Test retrieving an existing user message.
    """
    mock_message = {"_id": ObjectId(FAKE_ID), "message": "Hello again"}
    mock_db.__getitem__.return_value.find_one.return_value = mock_message

    response = client.get(f"/messages/user/{FAKE_ID}")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello again"


def test_get_user_message_not_found(mock_db):
    """
    Test retrieving a user message that does not exist.
    """
    mock_db.__getitem__.return_value.find_one.return_value = None

    response = client.get(f"/messages/user/{FAKE_ID}")
    assert response.status_code == 200
    assert response.json() == {"error": "User message not found"}


def test_delete_user_message_success(mock_db):
    """
    Test deleting a user message successfully.
    """
    mock_result = MagicMock(deleted_count=1)
    mock_db.__getitem__.return_value.delete_one.return_value = mock_result

    response = client.delete(f"/messages/user/{FAKE_ID}")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]


def test_delete_user_message_not_found(mock_db):
    """
    Test deleting a user message that does not exist.
    """
    mock_result = MagicMock(deleted_count=0)
    mock_db.__getitem__.return_value.delete_one.return_value = mock_result

    response = client.delete(f"/messages/user/{FAKE_ID}")
    assert response.status_code == 200
    assert response.json() == {"error": "User message not found"}


def test_get_system_message_found(mock_db):
    """
    Test retrieving an existing system message.
    """
    mock_message = {"_id": ObjectId(FAKE_ID), "message": "System log entry"}
    mock_db.__getitem__.return_value.find_one.return_value = mock_message

    response = client.get(f"/messages/system/{FAKE_ID}")
    assert response.status_code == 200
    assert response.json()["message"] == "System log entry"
    assert response.json()["_id"] == FAKE_ID


def test_get_system_message_not_found(mock_db):
    """
    Test retrieving a system message that does not exist.
    """
    mock_db.__getitem__.return_value.find_one.return_value = None

    response = client.get(f"/messages/system/{FAKE_ID}")
    assert response.status_code == 200
    assert response.json() == {"error": "System message not found"}


def test_delete_system_message_success(mock_db):
    """
    Test deleting a system message successfully.
    """
    mock_result = MagicMock(deleted_count=1)
    mock_db.__getitem__.return_value.delete_one.return_value = mock_result

    response = client.delete(f"/messages/system/{FAKE_ID}")
    assert response.status_code == 200
    assert response.json() == {"message": f"System message {FAKE_ID} deleted"}


def test_delete_system_message_not_found(mock_db):
    """
    Test deleting a system message that does not exist.
    """
    mock_result = MagicMock(deleted_count=0)
    mock_db.__getitem__.return_value.delete_one.return_value = mock_result

    response = client.delete(f"/messages/system/{FAKE_ID}")
    assert response.status_code == 200
    assert response.json() == {"error": "System message not found"}
    