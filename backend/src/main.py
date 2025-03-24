import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.llm_implementation import prompt_llm
from src.models import PromptRequest
from src.routes.messages import router as messages_router
from src.routes.llms import router as llms_router
from src.routes.responses import router as responses_router
from fastapi.middleware.cors import CORSMiddleware
from src.db import init_db
from src.db import get_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to MongoDB
    client, _ = init_db()
    app.mongodb_client = client
    
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
    # Generate the response using the LLM
    response = prompt_llm(prompt.system_message, prompt.user_message)
    
    # Insert the prompt messages and response into the "responses" collection
    db = get_database()
    responses = db.get_collection("responses")
    
    response_doc = {
        "system_message": prompt.system_message,
        "user_message": prompt.user_message,
        "response": response,
        "response_metadata": {
            "model": "llama3.1",
            "created_at": "2025-03-24T11:55:45.6765047Z",
            "done": True,
            "done_reason": "stop",
            "total_duration": 1494413400,
            "load_duration": 23515300,
            "prompt_eval_count": 25,
            "prompt_eval_duration": 3613800,
            "eval_count": 56,
            "eval_duration": 1465920900,
            "message": {
                "role": "assistant",
                "content": "",
                "images": None,
                "tool_calls": None
            }
        },
        "type": "ai",
        "name": None,
        "id": "run-8123189f-e685-4e2e-af60-505fa7a2aed6-0",
        "example": False,
        "tool_calls": [],
        "invalid_tool_calls": [],
        "usage_metadata": {
            "input_tokens": 25,
            "output_tokens": 56,
            "total_tokens": 81
        }
    }
    
    result = responses.insert_one(response_doc)
    print(f"Inserted response document with ID: {result.inserted_id}")
    
    return {"response_id": str(result.inserted_id), "response": response}


# @app.post("/prompt")
# async def prompt(prompt: PromptRequest):
#     response = prompt_llm(prompt.system_message, prompt.user_message)
#     return response