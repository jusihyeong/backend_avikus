from enum import Enum
from functools import lru_cache
from typing import Any

import yaml
from pydantic import Field, MySQLDsn
from pydantic.v1 import BaseSettings


class LogLevels(str, Enum):
    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"


class UvicornSettings(BaseSettings):
    host: str
    port: int = Field(ge=0, le=65535)
    reload: bool
    log_level: LogLevels


class ApiConfigSettings(BaseSettings):
    """Settings for FastAPI Server"""

    title: str = ""
    description: str = ""
    version: str
    docs_url: str


class DatabaseConnectionSettings(BaseSettings):
    mysql_user: str
    mysql_password: str
    mysql_database: str
    mysql_server: str
    mysql_port: int

    @property
    def mysql_uri(self) -> str:
        return MySQLDsn.build(
            scheme="mysql",
            username=self.mysql_user,
            password=self.mysql_password,
            host=self.mysql_server,
            port=self.mysql_port,
            path=f"{self.mysql_database}",

        )


class Settings(BaseSettings):
    uvicorn: UvicornSettings
    db_connection: DatabaseConnectionSettings
    api_config: ApiConfigSettings


def load_from_yaml() -> Any:
    import os
    curPath = os.getcwd()
    dir = "settings.yaml"
    if 'test' in curPath:
        dir = "../" + dir
    with open(dir) as fp:
        config = yaml.safe_load(fp)
    return config


@lru_cache()
def get_settings() -> Settings:
    yaml_config = load_from_yaml()
    settings = Settings(**yaml_config)
    return settings
