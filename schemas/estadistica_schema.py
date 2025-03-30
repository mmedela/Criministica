from pydantic import BaseModel
from typing import Optional

class EstadisticaBase(BaseModel):
    anio: int
    cantidad_hechos: Optional[int] = None
    cantidad_victimas: Optional[int] = None
    tasa_hechos: Optional[float] = None
    tasa_victimas: Optional[float] = None
    tasa_victimas_masc: Optional[float] = None
    tasa_victimas_fem: Optional[float] = None

class EstadisticaCreate(EstadisticaBase):
    provincia_id: int
    codigo_delito_snic_id: int

class EstadisticaUpdate(EstadisticaBase):
    pass

class EstadisticaResponse(EstadisticaBase):
    estadistica_id: int
    provincia_id: int
    codigo_delito_snic_id: int
    
    class Config:
        from_attributes = True
