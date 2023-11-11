from typing import Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.models.domains.avikus import Task
from src.models.schemas.avikus import TaskRegister, TaskUpdate
from src.repositories.crud_base import CRUDBase


class TaskRepo(CRUDBase[Task, TaskRegister, TaskUpdate]):

    async def create(self, db: Session, *, obj_in: TaskRegister) -> Task:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    async def update(self, db: Session, *, db_obj: Task, obj_in: Union[TaskUpdate, Dict[str, Any]]) -> Task:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def delete(self, db: Session, id: int):
        task = db.query(Task).get(id)
        db.delete(task)
        db.commit()

    async def getTask(self, db: Session, id: int):
        return db.query(Task).filter(Task.id == id).first()

    async def getTaskList(self, db: Session):
        return db.query(Task).all()


task = TaskRepo(Task)
