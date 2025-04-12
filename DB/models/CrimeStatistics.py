import sqlalchemy as sa
from .Base import *

class CrimeStatistics(Base):
    __tablename__ = 'crime_statistics'

    id = Column(Integer, primary_key=True)
    province_id = Column(Integer, sa.ForeignKey('provinces.province_id')) 
    crime_code_snic_id = Column(Integer, sa.ForeignKey('crimes.crime_code_snic_id'))
    year = Column(Integer)
    act_quantity = Column(Integer)
    victim_quantity = Column(Integer)
    male_victims_quantity = Column(Integer)
    female_victims_quantity = Column(Integer)
    victim_quantity_sd = Column(Integer)
    act_rate = Column(sa.Numeric)
    victim_rate = Column(sa.Numeric)
    male_victims_rate = Column(sa.Numeric)
    female_victims_rate = Column(sa.Numeric)
    
    provinces = relationship("Province", back_populates="statistics")
    crimes = relationship("Crime", back_populates="statistics")
    
    __table_args__ = (
        sa.UniqueConstraint('province_id', 'crime_code_snic_id', 'year', name='uq_statistics'),
    )
    
    def __repr__(self):
        return f"<CrimeStatistics(id={self.id}, year={self.year}, province={self.provinces.province_id}, crime={self.crimes.crime_code_snic_id})>"