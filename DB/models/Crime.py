from .Base import *

class Crime(Base):
    __tablename__ = 'crimes'

    crime_code_snic_id = Column(Integer, primary_key=True)
    crime_code_snic_name = Column(String)
    
    # Relación con estadísticas de delitos
    statistics = relationship('CrimeStatistics', back_populates='crimes')
    
    def __repr__(self):
        return f"<Crime(id={self.crime_code_snic_id}, name={self.crime_code_snic_name})>"