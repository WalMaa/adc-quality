from fastapi import APIRouter


router = APIRouter(prefix="/responses")

# Get all responses
@router.get("/")
async def list_responses():
    # TODO: get responses from db
    return ["Response 1", "Response 2"]

# Get a response
@router.get("/{response_id}")
async def get_response(response_id: int):
    # TODO: get response from db
    return f"Response {response_id}"

# Delete a response
@router.delete("/{response_id}")
async def delete_response(response_id: int):
    # TODO: delete response from db
    return f"Response {response_id} deleted"
