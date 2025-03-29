from Base import *

class Provincia(Base):
    __tablename__ = 'provincias'

    provincia_id = Column(String, primary_key=True)
    provincia_nombre = Column(String)
