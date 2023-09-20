from fastapi import Request
from fastapi.responses import JSONResponse

from main import app


class ValidationError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=exc.status_code,
        content={}
    )