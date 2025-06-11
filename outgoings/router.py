from fastapi import APIRouter
from fastapi.responses import JSONResponse

outgoings_router = APIRouter(prefix="/outgoings", tags=["outgoings"])


@outgoings_router.post("/save")
def outgoings():
    """
    Endpoint to save incoming data.
    """
    # Here you would implement the logic to save outgoings data
    return JSONResponse(
            status_code=200,
            content={
        "message": "Incoming data saved successfully.",
            "success": 1
            }
    )