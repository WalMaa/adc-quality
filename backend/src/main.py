from fastapi import FastAPI
from pymongo import MongoClient
from contextlib import asynccontextmanager
from src.llm_implementation import prompt_llm
from src.models import PromptRequest
from src.routes.messages import router as messages_router
from src.routes.llms import router as llms_router
from src.routes.responses import router as responses_router
from fastapi.middleware.cors import CORSMiddleware

async def connect_to_mongo(app: FastAPI):
    try:
        app.mongodb_client = MongoClient("mongodb://root:pass@mongo:27017/", connectTimeoutMS=5000, socketTimeoutMS=5000, serverSelectionTimeoutMS=5000)
        app.database = app.mongodb_client["mydb"]
        app.mongodb_client.admin.command('ping')
        print("Connected to MongoDB")
    except Exception as e:
        print(f"An error occurred while connecting to MongoDB: {e}")
    
    
    
async def close_mongo_connection(app: FastAPI):
    app.mongodb_client.close()
    print("Closed connection to MongoDB")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo(app)
    yield
    await close_mongo_connection(app)

    
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
    print("Response: ", response)
    return response