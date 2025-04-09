from pydantic import BaseModel
from typing import Optional

class ProvinceBase(BaseModel):
    province_name: str

class ProvinceCreate(ProvinceBase):
    population: Optional[int] = None

class ProvinceUpdate(BaseModel):
    population: Optional[int] = None

class ProvinceResponse(ProvinceBase):
    province_id: int
    population: Optional[int] = None
    
    class Config:
        from_attributes = True
