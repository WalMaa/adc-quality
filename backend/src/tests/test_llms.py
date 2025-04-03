import sys
import importlib.util
from pathlib import Path
import requests
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

llms_path = Path(__file__).resolve().parents[2] / "src" / "routes" / "llms.py"
spec = importlib.util.spec_from_file_location("llms_module", llms_path)
llms_module = importlib.util.module_from_spec(spec)
sys.modules["llms_module"] = llms_module
spec.loader.exec_module(llms_module)

app = FastAPI()
app.include_router(llms_module.router)
client = TestClient(app)


@patch("llms_module.requests.get")
def test_get_available_llms_success(mock_requests_get):
    """
    Test that /llms/ returns a list of available models when the request succeeds.
    """
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "models": [{"name": "llama2"}, {"name": "mistral"}]
    }
    mock_requests_get.return_value = mock_response

    response = client.get("/llms/")
    assert response.status_code == 200
    assert response.json() == {
        "llms": [
            {"name": "llama2", "status": "available"},
            {"name": "mistral", "status": "available"}
        ]
    }


@patch("llms_module.requests.get", side_effect=requests.exceptions.RequestException("Connection failed"))
def test_get_available_llms_failure(mock_requests_get):
    """
    Test that /llms/ returns 500 if fetching models from Ollama fails.
    """
    response = client.get("/llms/")
    assert response.status_code == 500
    assert "Failed to fetch models" in response.json()["detail"]


@patch("llms_module.requests.get")
def test_select_llm_success(mock_requests_get):
    """
    Test that /llms/select sets the selected model if it's available.
    """
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "models": [{"name": "llama2"}, {"name": "mistral"}]
    }
    mock_requests_get.return_value = mock_response

    response = client.post("/llms/select", json={"model_name": "llama2"})
    assert response.status_code == 200
    assert response.json() == {"message": "Selected model set to llama2"}
    assert llms_module.get_current_selected_llm() == "llama2"


@patch("llms_module.requests.get")
def test_select_llm_invalid_model(mock_requests_get):
    """
    Test that /llms/select returns 400 if the model name is not in the list.
    """
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "models": [{"name": "llama2"}]
    }
    mock_requests_get.return_value = mock_response

    response = client.post("/llms/select", json={"model_name": "unknown"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Model not available"


@patch("llms_module.requests.get", side_effect=requests.exceptions.RequestException("API error"))
def test_select_llm_api_failure(mock_requests_get):
    """
    Test that /llms/select returns 500 if fetching model list fails.
    """
    response = client.post("/llms/select", json={"model_name": "llama2"})
    assert response.status_code == 500
    assert "Failed to fetch models" in response.json()["detail"]


def test_get_selected_llm_endpoint_success():
    """
    Test that /llms/selected returns the current model if one is selected.
    """
    llms_module.set_selected_llm("llama2")
    response = client.get("/llms/selected")
    assert response.status_code == 200
    assert response.json() == {"selected_llm": "llama2"}


def test_get_selected_llm_endpoint_not_set():
    """
    Test that /llms/selected returns 404 if no model is selected.
    """
    llms_module._selected_llm = None  # Ensure no model is selected
    response = client.get("/llms/selected")
    assert response.status_code == 404
    assert response.json()["detail"] == "No model selected"
