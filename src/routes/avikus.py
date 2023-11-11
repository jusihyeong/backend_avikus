from fastapi import APIRouter, Depends, Path
from fastapi_etag import Etag
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

from src import repositories
from src.core.databases.database import get_db
from src.core.responses import ServiceBaseResponse, success_response
from src.models.schemas.avikus import Task, TaskRegister, TaskUpdate

route = APIRouter()


@route.post("/create", response_model=Task)
async def setTask(
        taskRegister: TaskRegister,
        db: Session = Depends(get_db)
) -> JSONResponse:
    task = await repositories.task.create(db=db, obj_in=taskRegister)
    return success_response(task, status_code=HTTP_201_CREATED)


async def get_task_read_etag(request: Request):
    id = request.path_params.get("id")
    return f"task_etag_id_{id}"


@route.get("/read/{id}", dependencies=[Depends(Etag(get_task_read_etag,
                                                    extra_headers={"Cache-Control": "public, max-age: 30"},
                                                    ))])
async def getTask(
        id: int = Path(..., gt=0),
        db: Session = Depends(get_db)
) -> JSONResponse:
    task = await repositories.task.getTask(db=db, id=id)
    return success_response(task)


@route.put("/update/{id}", response_model=Task)
async def updateTask(
        taskUpdate: TaskUpdate,
        id: int = Path(..., gt=0),
        db: Session = Depends(get_db)
) -> JSONResponse:
    task = await repositories.task.getTask(db=db, id=id)
    task = await repositories.task.update(db=db, db_obj=task, obj_in=taskUpdate)
    return success_response(task, status_code=HTTP_201_CREATED)


@route.delete("/delete/{id}", response_model=ServiceBaseResponse)
async def deleteTask(
        id: int = Path(..., gt=0),
        db: Session = Depends(get_db)
) -> JSONResponse:
    await repositories.task.delete(db=db, id=id)
    return success_response()
