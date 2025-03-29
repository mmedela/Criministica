from Base import *

class EstadisticaDelito(Base):
    __tablename__ = 'estadisticas_delitos'

    id = Column(Integer, primary_key=True)
    provincia_id = Column(String)
    anio = Column(Date)
    codigo_delito_snic_id = Column(Integer)
    cantidad_hechos = Column(Integer)
    cantidad_victimas = Column(Integer)
    cantidad_victimas_masc = Column(Integer)
    cantidad_victimas_fem = Column(Integer)
    cantidad_victimas_sd = Column(Integer)
    tasa_hechos = Column(Integer)
    tasa_victimas = Column(Integer)
    tasa_victimas_masc = Column(Integer)
    tasa_victimas_fem = Column(Integer)