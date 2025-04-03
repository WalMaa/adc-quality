import sys
import importlib.util
from pathlib import Path
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from bson import ObjectId

responses_path = Path(__file__).resolve().parents[2] / "src" / "routes" / "responses.py"
spec = importlib.util.spec_from_file_location("responses_module", responses_path)
responses_module = importlib.util.module_from_spec(spec)
sys.modules["responses_module"] = responses_module
spec.loader.exec_module(responses_module)

app = FastAPI()
app.include_router(responses_module.router)
client = TestClient(app)

FAKE_ID = str(ObjectId())


@pytest.fixture
def mock_db():
    """
    Fixture to patch get_database and yield a mock DB.
    """
    with patch("responses_module.get_database") as mock_get_db:
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        yield mock_db


def test_list_responses(mock_db):
    """
    Test listing all responses.
    """
    mock_docs = [{"_id": ObjectId(), "message": "test response"}]
    mock_db.get_collection.return_value.find.return_value = mock_docs

    response = client.get("/responses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["message"] == "test response"


def test_get_response_found(mock_db):
    """
    Test retrieving an existing response by ID.
    """
    mock_doc = {"_id": ObjectId(FAKE_ID), "message": "response found"}
    mock_db.get_collection.return_value.find_one.return_value = mock_doc

    response = client.get(f"/responses/{FAKE_ID}")
    assert response.status_code == 200
    assert response.json()["message"] == "response found"
    assert response.json()["_id"] == FAKE_ID


def test_get_response_not_found(mock_db):
    """
    Test retrieving a response that does not exist.
    """
    mock_db.get_collection.return_value.find_one.return_value = None

    response = client.get(f"/responses/{FAKE_ID}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Response not found"


def test_delete_response_success(mock_db):
    """
    Test successfully deleting a response by ID.
    """
    mock_result = MagicMock(deleted_count=1)
    mock_db.get_collection.return_value.delete_one.return_value = mock_result

    response = client.delete(f"/responses/{FAKE_ID}")
    assert response.status_code == 200
    assert f"Response {FAKE_ID} deleted" in response.json()["message"]


def test_delete_response_not_found(mock_db):
    """
    Test deleting a response that does not exist.
    """
    mock_result = MagicMock(deleted_count=0)
    mock_db.get_collection.return_value.delete_one.return_value = mock_result

    response = client.delete(f"/responses/{FAKE_ID}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Response not found"
