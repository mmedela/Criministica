from Base import *

class Provincia(Base):
    __tablename__ = 'provincias'

    provincia_id = Column(String, primary_key=True)
    provincia_nombre = Column(String)
    
    # Relación con estadísticas de delitos
    estadisticas = relationship('EstadisticaDelito', back_populates='provincia')
    
    def __repr__(self):
        return f"<Provincia(id={self.id}, nombre={self.nombre})>"
