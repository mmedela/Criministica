from models.Base import Base, engine
from sqlalchemy.orm import sessionmaker
from models.Province import Province  # Importa el modelo
from models.Crime import Crime
from models.CrimeStatistics import CrimeStatistics
Base.metadata.create_all(engine)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

print("Database and tables created successfully.")