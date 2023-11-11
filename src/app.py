from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_etag import add_exception_handler
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.core.databases.database import db_session
from src.core.responses import error_response

from src.routes import api_router
from settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.api_config.title,
    description=settings.api_config.description,
    version=settings.api_config.version,
    docs_url=settings.api_config.docs_url
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_exception_handler(app)


@app.on_event("startup")
async def startup_event() -> None:
    db_session.begin()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    db_session.close()


@app.exception_handler(RequestValidationError)
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return error_response(errors=str(exc), status_code=status.HTTP_400_BAD_REQUEST)


app.include_router(api_router)
