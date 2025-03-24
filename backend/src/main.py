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
    response = prompt_llm(prompt.system_message, prompt.user_message)
    return response