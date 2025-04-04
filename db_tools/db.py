from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


engine = create_engine(os.getenv("DB_URL"), echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
