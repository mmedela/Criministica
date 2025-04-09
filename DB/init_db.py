from DB.models.Base import Base, engine
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(engine)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

print("Database and tables created successfully.")