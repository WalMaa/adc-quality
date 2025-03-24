from fastapi import APIRouter

llms_available = ["llama3.1"]
                  
router = APIRouter(prefix="/llms")
# 2. Get available LLM models
@router.get("/")
async def get_available_llms():
    return {"llms": [{"name": llm, "status": "available"} for llm in llms_available]}