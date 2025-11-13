from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:///activity.db"
# TODO: Look into why following is needed for sqlite
engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    # TODO: Look into above aswell
    bind=engine,
)

base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
