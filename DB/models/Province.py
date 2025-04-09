from .Base import *

class Province(Base):
    __tablename__ = 'provinces'

    province_id = Column(Integer, primary_key=True)
    province_name = Column(String)
    population = Column(Integer, nullable=True)

    # Relación con estadísticas de delitos
    statistics = relationship('EstadisticaDelito', back_populates='provinces')

    def __repr__(self):
        return f"<Province(id={self.province_id}, name={self.province_name}, population={self.population})>"
