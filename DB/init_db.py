from models.Base import Base, engine
from sqlalchemy import create_engine

Base.metadata.create_all(engine)

print("Base de datos y tablas creadas con éxito.")