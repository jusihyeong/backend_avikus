import datetime
from typing import List, Optional

from pydantic import BaseModel


class Task(BaseModel):
    id: int
    name: Optional[str]
    content: Optional[str] = None
    create: Optional[datetime.datetime] = datetime.datetime.now()


class TaskList(Task):
    data: List[Task]


class TaskRegister(Task):
    id: Optional[int] = None
    name: Optional[str]
    content: Optional[str] = None
    create: Optional[datetime.datetime] = datetime.datetime.now()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "John", "content": "something"},
                {"name": "Alice", "content": "anything"}
            ]
        }
    }


class TaskUpdate(Task):
    id: Optional[int] = None
    name: Optional[str] = None
    content: Optional[str] = None
    create: Optional[datetime.datetime] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "John2"},
                {"content": "anything2"}
            ]
        }
    }