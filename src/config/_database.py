from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ._settings import get_settings

engine = create_engine(get_settings().db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
