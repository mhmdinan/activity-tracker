from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:///activity.db"

engine = create_engine(
    DB_URL,
    # TODO: Look into why following is needed for sqlite
    connect_args={"check_same_thread_: False"},
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