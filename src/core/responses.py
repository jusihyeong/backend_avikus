from typing import Any, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse


def success_response(response_data: Optional[Any] = None, status_code: int = status.HTTP_200_OK,) -> JSONResponse:
    response_json = {"success": True}

    if response_data is not None:
        response_json["data"] = jsonable_encoder(response_data)

    return JSONResponse(response_json, status_code=status_code)


def error_response(errors: Optional[Any] = None,status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,) -> JSONResponse:
    response_json = {"success": False}
    if errors is not None:
        response_json["errors"] = jsonable_encoder(errors)

    return JSONResponse(response_json, status_code=status_code)


class ServiceBaseResponse(BaseModel):
    success: bool