from models.Base import Base, engine

Base.metadata.create_all(engine)

print("Base de datos y tablas creadas con éxito.")