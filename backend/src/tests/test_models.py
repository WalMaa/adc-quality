import pytest
from backend.src import models


def test_prompt_request_valid():
    """
    Test that PromptRequest accepts valid input with both required fields present.
    """
    data = {
        "system_message": "You are a helpful assistant.",
        "user_message": "Hello!"
    }
    prompt = models.PromptRequest(**data)
    assert prompt.system_message == "You are a helpful assistant."
    assert prompt.user_message == "Hello!"


def test_prompt_request_missing_field():
    """
    Test that PromptRequest raises a validation error when 'user_message' is missing.
    """
    data = {
        "system_message": "You are a helpful assistant."
    }
    with pytest.raises(Exception) as e:
        models.PromptRequest(**data)
    assert "user_message" in str(e.value)


def test_message_request_valid():
    """
    Test that MessageRequest accepts valid input when the required 'message' field is provided.
    """
    message = models.MessageRequest(message="Hey there!")
    assert message.message == "Hey there!"


def test_message_request_missing_field():
    """
    Test that MessageRequest raises a validation error when 'message' is missing.
    """
    with pytest.raises(Exception):
        models.MessageRequest()
