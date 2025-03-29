from .Base import *

class Provincia(Base):
    __tablename__ = 'provincias'

    provincia_id = Column(Integer, primary_key=True)
    provincia_nombre = Column(String)
    
    # Relación con estadísticas de delitos
    estadisticas = relationship('EstadisticaDelito', back_populates='provincia')
    
    def __repr__(self):
        return f"<Provincia(id={self.provincia_id}, nombre={self.provincia_nombre})>"
