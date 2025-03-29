from Base import *

class Delito(Base):
    __tablename__ = 'delitos'

    codigo_delito_snic_id = Column(Integer, primary_key=True)
    codigo_delito_snic_nombre = Column(String)