
import sys
import importlib.util
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

llm_path = Path(__file__).resolve().parents[2] / "src" / "llm_implementation.py"
spec = importlib.util.spec_from_file_location("llm_module", llm_path)
llm_module = importlib.util.module_from_spec(spec)
sys.modules["llm_module"] = llm_module
spec.loader.exec_module(llm_module)

@pytest.fixture
def mock_get_current_selected_llm_none():
    with patch("backend.src.llm_implementation.get_current_selected_llm", return_value=None):
        yield


def test_prompt_llm_raises_if_no_model_selected(mock_get_current_selected_llm_none):
    """
    Test that prompt_llm() raises a ValueError if no LLM model is selected.
    """
    with pytest.raises(ValueError, match="No LLM model selected"):
        llm_module.prompt_llm("test", "system")


@patch("llm_module.get_current_selected_llm")
@patch("llm_module.ChatOllama")
def test_prompt_llm_creates_llm_instance_and_invokes(mock_chat_ollama, mock_get_llm):
    """
    Test that prompt_llm() creates a ChatOllama instance, formats the prompt,
    and calls invoke() with the formatted prompt.
    """
    mock_get_llm.return_value = "llama2"
    mock_llm_instance = MagicMock()
    mock_llm_instance.model = "llama2"
    mock_llm_instance.invoke.return_value = "Mock response"

    mock_chat_ollama.return_value = mock_llm_instance

    response = llm_module.prompt_llm("Hello", "You are helpful")

    assert response == "Mock response"
    mock_chat_ollama.assert_called_once_with(model="llama2", base_url="http://host.docker.internal:11434")
    mock_llm_instance.invoke.assert_called_once()
    assert "Hello" in mock_llm_instance.invoke.call_args[0][0]
    assert "You are helpful" in mock_llm_instance.invoke.call_args[0][0]


@patch("llm_module.get_current_selected_llm")
@patch("llm_module.ChatOllama")
def test_prompt_llm_reuses_llm_instance_if_same_model(mock_chat_ollama, mock_get_llm):
    """
    Test that prompt_llm() reuses the existing ChatOllama instance if the model is the same.
    """
    llm_module.llm = None

    mock_get_llm.return_value = "llama2"

    mock_llm_instance = MagicMock()
    mock_llm_instance.model = "llama2"
    mock_llm_instance.invoke.return_value = "First call response"
    mock_chat_ollama.return_value = mock_llm_instance

    # First call — should create a new instance
    llm_module.prompt_llm("First", "System")

    # Second call — should reuse the same instance
    mock_llm_instance.invoke.return_value = "Reused instance response"
    mock_llm_instance.invoke.reset_mock()
    mock_chat_ollama.reset_mock()

    response = llm_module.prompt_llm("Second", "System")

    assert response == "Reused instance response"
    mock_chat_ollama.assert_not_called()
    mock_llm_instance.invoke.assert_called_once()
