from pydantic import BaseModel
from typing import Optional

class ProvinciaBase(BaseModel):
    provincia_nombre: str

class ProvinciaCreate(ProvinciaBase):
    poblacion: Optional[int] = None

class ProvinciaUpdate(BaseModel):
    poblacion: Optional[int] = None

class ProvinciaResponse(ProvinciaBase):
    provincia_id: int
    poblacion: Optional[int] = None
    
    class Config:
        from_attributes = True
