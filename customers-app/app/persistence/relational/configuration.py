from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from dotenv import load_dotenv

import os
load_dotenv()

username = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
port = os.getenv('PORT')
test_port = 3308

url = f'mysql://{username}:{password}@mysql:{port}/{database}'
engine = create_engine(url, echo=True)

test_url = f'mysql://{username}:{password}@mysql-test:{test_port}/{database}'
test_engine = create_engine(url, echo=True)
# ==========================================================================


class Base(DeclarativeBase):
    pass
# ==========================================================================


def create_session() -> Session:
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    return Session()
