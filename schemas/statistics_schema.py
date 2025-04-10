from pydantic import BaseModel
from typing import Optional

class StatisticsBase(BaseModel):
    year: int
    act_quantity: Optional[int] = None
    victim_quantity: Optional[int] = None
    act_rate: Optional[float] = None
    victim_rate: Optional[float] = None
    male_victims_rate: Optional[float] = None
    female_victims_rate: Optional[float] = None

class StatisticsCreate(StatisticsBase):
    province_id: int
    crime_code_snic_id: int

class StatisticsUpdate(StatisticsBase):
    pass

class StatisticsResponse(StatisticsBase):
    id: int
    province_id: int
    crime_code_snic_id: int
    year: int
    act_quantity: Optional[int] = 0
    victim_quantity: Optional[int] = 0
    male_victims_quantity: Optional[int] = 0
    female_victims_quantity: Optional[int] = 0
    victim_quantity_sd: Optional[int] = 0
    act_rate: Optional[float] = 0.0
    victim_rate: Optional[float] = 0.0
    male_victims_rate: Optional[float] = 0.0
    female_victims_rate: Optional[float] = 0.0
    
    class Config:
        from_attributes = True
