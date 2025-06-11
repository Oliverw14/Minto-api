from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


from incomings.router import incomings_router
from outgoings.router import outgoings_router


def get_application() -> FastAPI:
    app = FastAPI(redirect_slashes=False )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=['*']
    )
    app.include_router(incomings_router)
    app.include_router(outgoings_router)

    # Global excpetion handling
    @app.exception_handler(ValueError)
    async def value_error_exception_handler(request, exc):
        print(exc, flush=True)
        return JSONResponse(
            status_code=400,
            content={"message": "There was an error handling your request"},
        )
    
    @app.exception_handler(KeyError)
    async def key_error_exception_handler(request, exc):
        print(exc, flush=True)
        return JSONResponse(
            status_code=400,
            content={"message": "There was an error handling your request"},
        )
    
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request, exc):
        print(exc, flush=True)
        return JSONResponse(
            status_code=422,
            content={"message": "There was an error handling your request."},
        )
    
    @app.exception_handler(AttributeError)
    async def attr_error_exception_handler(request, exc):
        print(exc, flush=True)
        return JSONResponse(
            status_code=400,
            content={"message": "There was an error handling your request"},
        )

    return app

app = get_application()
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)