from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_usr}:{settings.db_pwd}@{settings.db_host}/{settings.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Connect to a database
# HOST = "localhost"
# DATABASE = "fastapi"
# USER = "postgres"
# PASSWORD = "October01"
# while True:
#     try:
#         conn = psycopg2.connect(
#             host=HOST,
#             database=DATABASE,
#             user=USER,
#             password=PASSWORD,
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         break
#     except Exception as e:
#         print("Connecting to database failed")
#         print(e)
#         time.sleep(1)
