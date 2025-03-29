from fastapi import APIRouter, HTTPException, Body
import requests

router = APIRouter(prefix="/llms")

@router.get("/")
async def get_available_llms():
    try:
        response = requests.get("http://host.docker.internal:11434/api/tags")
        response.raise_for_status()
        data = response.json()
        
        llms_available = data.get("models", [])
        
        return {"llms": [{"name": llm["name"], "status": "available"} for llm in llms_available]}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch models: {str(e)}")

selected_llm = None

@router.post("/select")
async def select_llm(model_name: str = Body(..., embed=True)):
    global selected_llm
    try:
        response = requests.get("http://host.docker.internal:11434/api/tags")
        response.raise_for_status()
        data = response.json()
        
        llms_available = [model["name"] for model in data.get("models", [])]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch models: {str(e)}")

    if model_name not in llms_available:
        raise HTTPException(status_code=400, detail="Model not available")
    
    selected_llm = model_name
    return {"message": f"Selected model set to {selected_llm}"}



@router.get("/selected")
async def get_selected_llm():
    if not selected_llm:
        raise HTTPException(status_code=404, detail="No model selected")
    return {"selected_llm": selected_llm}