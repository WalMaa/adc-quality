from fastapi import APIRouter, HTTPException, Body
import requests

router = APIRouter(prefix="/llms")

_selected_llm = None

def get_current_selected_llm():
    return _selected_llm

def set_selected_llm(model_name: str):
    global _selected_llm
    _selected_llm = model_name

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

@router.post("/select")
async def select_llm(model_name: str = Body(..., embed=True)):
    try:
        response = requests.get("http://host.docker.internal:11434/api/tags")
        response.raise_for_status()
        data = response.json()
        
        llms_available = [model["name"] for model in data.get("models", [])]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch models: {str(e)}")

    if model_name not in llms_available:
        raise HTTPException(status_code=400, detail="Model not available")
    
    set_selected_llm(model_name)
    return {"message": f"Selected model set to {model_name}"}

@router.get("/selected")
async def get_selected_llm_endpoint():
    current_llm = get_current_selected_llm()
    if not current_llm:
        raise HTTPException(status_code=404, detail="No model selected")
    return {"selected_llm": current_llm}