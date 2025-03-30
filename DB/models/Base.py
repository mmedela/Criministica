from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

engine = create_engine(DATABASE_URL, echo=True)

