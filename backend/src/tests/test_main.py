import requests
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from bson import ObjectId
from backend.src import main

client = TestClient(main.app)
FAKE_ID = str(ObjectId())


def test_root_returns_hello_world():
    """
    Test that the root endpoint returns the expected message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@patch("backend.src.main.prompt_llm")
@patch("backend.src.main.get_database")
def test_prompt_endpoint_success(mock_get_db, mock_prompt_llm):
    """
    Test that the prompt endpoint calls the LLM and stores the result in MongoDB.
    """
    mock_response = MagicMock()
    mock_response.content = "Mocked response content"
    mock_prompt_llm.return_value = mock_response

    mock_collection = MagicMock()
    mock_collection.insert_one.return_value.inserted_id = ObjectId(FAKE_ID)
    mock_get_db.return_value.get_collection.return_value = mock_collection

    payload = {
        "system_message": "You are helpful.",
        "user_message": "Tell me a joke."
    }

    response = client.post("/prompt", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["response_id"] == FAKE_ID
    assert data["response"] == "Mocked response content"

    mock_prompt_llm.assert_called_once_with("You are helpful.", "Tell me a joke.")
    mock_collection.insert_one.assert_called_once_with({
        "system_message": "You are helpful.",
        "user_message": "Tell me a joke.",
        "response": "Mocked response content"
    })


@patch("backend.src.routes.llms.set_selected_llm")
@patch("backend.src.main.requests.get")
@patch("backend.src.main.init_db")
def test_lifespan_startup_logic(mock_init_db, mock_requests_get, mock_set_llm):
    """
    Test that the FastAPI lifespan event initializes MongoDB and selects the first LLM.
    """
    from backend.src.main import app

    mock_client = MagicMock()
    mock_init_db.return_value = (mock_client, MagicMock())

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "models": [{"name": "llama2"}]
    }
    mock_requests_get.return_value = mock_response

    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200

    mock_init_db.assert_called_once()
    mock_requests_get.assert_called_once()
    mock_set_llm.assert_called_once_with("llama2")
    mock_client.close.assert_called_once()


@patch("backend.src.routes.llms.set_selected_llm")
@patch("backend.src.main.requests.get")
@patch("backend.src.main.init_db")
def test_lifespan_no_llms(mock_init_db, mock_requests_get, mock_set_llm):
    """
    Test that the lifespan prints a message when no LLMs are available.
    """
    from backend.src.main import app

    mock_client = MagicMock()
    mock_init_db.return_value = (mock_client, MagicMock())

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"models": []}
    mock_requests_get.return_value = mock_response

    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200

    mock_set_llm.assert_not_called()
    mock_client.close.assert_called_once()


@patch("backend.src.routes.llms.set_selected_llm")
@patch("backend.src.main.requests.get", side_effect=requests.exceptions.RequestException("API failure"))
@patch("backend.src.main.init_db")
def test_lifespan_llm_fetch_failure(mock_init_db, mock_requests_get, mock_set_llm):
    """
    Test that the lifespan handles LLM fetch failure gracefully.
    """
    from backend.src.main import app

    mock_client = MagicMock()
    mock_init_db.return_value = (mock_client, MagicMock())

    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200

    mock_set_llm.assert_not_called()
    mock_requests_get.assert_called_once()
    mock_client.close.assert_called_once()
