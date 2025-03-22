from fastapi import FastAPI
from pymongo import MongoClient
from contextlib import asynccontextmanager


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


@app.get("/")
async def root():
    return {"message": "Hello World"}