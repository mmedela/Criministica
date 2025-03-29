from .Base import *

class Delito(Base):
    __tablename__ = 'delitos'

    codigo_delito_snic_id = Column(Integer, primary_key=True)
    codigo_delito_snic_nombre = Column(String)
    
    # Relación con estadísticas de delitos
    estadisticas = relationship('EstadisticaDelito', back_populates='delito')
    
    def __repr__(self):
        return f"<Delito(id={self.codigo_delito_snic_id}, nombre={self.codigo_delito_snic_nombre})>"