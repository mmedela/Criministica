import sqlalchemy as sa
from .Base import *

class EstadisticaDelito(Base):
    __tablename__ = 'estadisticas_delitos'

    id = Column(Integer, primary_key=True)
    provincia_id = Column(Integer, sa.ForeignKey('provincias.provincia_id')) 
    codigo_delito_snic_id = Column(Integer, sa.ForeignKey('delitos.codigo_delito_snic_id'))
    anio = Column(Integer)
    cantidad_hechos = Column(Integer)
    cantidad_victimas = Column(Integer)
    cantidad_victimas_masc = Column(Integer)
    cantidad_victimas_fem = Column(Integer)
    cantidad_victimas_sd = Column(Integer)
    tasa_hechos = Column(sa.Numeric)
    tasa_victimas = Column(sa.Numeric)
    tasa_victimas_masc = Column(sa.Numeric)
    tasa_victimas_fem = Column(sa.Numeric)
    
    provincia = relationship("Provincia", back_populates="estadisticas")
    delito = relationship("Delito", back_populates="estadisticas")
    
    __table_args__ = (
        sa.UniqueConstraint('provincia_id', 'codigo_delito_snic_id', 'anio', name='uq_estadisticas'),
    )
    
    def __repr__(self):
        return f"<EstadisticaDelito(id={self.id}, anio={self.anio}, provincia={self.provincia.provincia_id}, delito={self.delito.codigo_delito_snic_id})>"