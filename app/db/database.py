# Připojení databáze

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def prepare_session(DB_URL):
    # db_string = "postgresql://postgres:postgres@localhost/metrologie"

    engine = create_engine(DB_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return SessionLocal, engine


Base = declarative_base()
