from fastapi import APIRouter
from fastapi.responses import JSONResponse

incomings_router = APIRouter(prefix="/incomings", tags=["incomings"])


@incomings_router.post("/save")
def save_incoming():
    """
    Endpoint to save incoming data.
    """
    # Here you would implement the logic to save incoming data
    return JSONResponse(
            status_code=200,
            content={
        "message": "Incoming data saved successfully.",
            "success": 1
            }
    )