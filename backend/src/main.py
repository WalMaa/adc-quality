import sys
from pathlib import Path

current_dir = Path(__file__).resolve()
backend_src = current_dir.parent
if str(backend_src) not in sys.path:
    sys.path.insert(0, str(backend_src)) # pragma: no cover

import logging
import requests
from fastapi import FastAPI
from contextlib import asynccontextmanager
from llm_implementation import prompt_llm
from models import PromptRequest
from routes.messages import router as messages_router
from routes.llms import router as llms_router, set_selected_llm
from routes.responses import router as responses_router
from fastapi.middleware.cors import CORSMiddleware
from db import init_db, get_database
import repository

@asynccontextmanager
async def lifespan(app: FastAPI):
    repository.init_db()

    # Connect to MongoDB
    client, _ = init_db()
    app.mongodb_client = client

    # Fetch available LLMs and set the first one as the selected model
    try:
        response = requests.get("http://host.docker.internal:11434/api/tags")
        response.raise_for_status()
        data = response.json()
        llms_available = data.get("models", [])

        if llms_available:
            from backend.src.routes.llms import set_selected_llm
            set_selected_llm(llms_available[0]["name"])
            print(f"Selected LLM on startup: {llms_available[0]['name']}")
        else:
            print("No LLMs available to select on startup.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch models on startup: {str(e)}")

    yield

    # Disconnect from MongoDB
    if hasattr(app, 'mongodb_client') and app.mongodb_client:
        app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(messages_router)
app.include_router(llms_router)
app.include_router(responses_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/prompt")
async def prompt(prompt: PromptRequest):
    response = prompt_llm(prompt.system_message, prompt.user_message)

    response_content = response.content

    response_doc = {
        "system_message": prompt.system_message,
        "user_message": prompt.user_message,
        "response": response_content
    }

    # Insert the prompt messages and response into the "responses" collection
    db = get_database()
    responses = db.get_collection("responses")


    result = responses.insert_one(response_doc)
    print(f"Inserted response document with ID: {result.inserted_id}")

    return {"response_id": str(result.inserted_id), "response": response_content}


# @app.post("/prompt")
# async def prompt(prompt: PromptRequest):
#     response = prompt_llm(prompt.system_message, prompt.user_message)
#     return response