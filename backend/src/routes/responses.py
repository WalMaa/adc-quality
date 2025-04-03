import sys
import importlib.util
from pathlib import Path
from fastapi import APIRouter, HTTPException
from bson import ObjectId

db_path = Path(__file__).resolve().parents[2] / "src" / "db.py"
spec_db = importlib.util.spec_from_file_location("db_module", db_path)
db_module = importlib.util.module_from_spec(spec_db)
sys.modules["db_module"] = db_module
spec_db.loader.exec_module(db_module)

get_database = db_module.get_database

router = APIRouter(prefix="/responses")

# Get all responses
@router.get("/")
async def list_responses():
    db = get_database()
    responses_collection = db.get_collection("responses")
    responses = list(responses_collection.find())
    
    for response in responses:
        response["_id"] = str(response["_id"])
    
    return responses

# Get a response
@router.get("/{response_id}")
async def get_response(response_id: str):
    db = get_database()
    responses_collection = db.get_collection("responses")
    response = responses_collection.find_one({"_id": ObjectId(response_id)})
    
    if response:
        response["_id"] = str(response["_id"])
        return response
    raise HTTPException(status_code=404, detail="Response not found")

# Delete a response
@router.delete("/{response_id}")
async def delete_response(response_id: str):
    db = get_database()
    responses_collection = db.get_collection("responses")
    result = responses_collection.delete_one({"_id": ObjectId(response_id)})
    
    if result.deleted_count == 1:
        return {"message": f"Response {response_id} deleted"}
    raise HTTPException(status_code=404, detail="Response not found")