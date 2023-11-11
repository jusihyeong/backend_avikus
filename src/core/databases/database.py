from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

from settings import get_settings

settings = get_settings()

engine = create_engine(str(settings.db_connection.mysql_uri),
                       echo=False,
                       pool_size=10,
                       max_overflow=10)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
