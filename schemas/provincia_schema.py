from pydantic import BaseModel

class ProvinciaBase(BaseModel):
    provincia_nombre: str

class ProvinciaCreate(ProvinciaBase):
    pass

class ProvinciaUpdate(ProvinciaBase):
    pass

class ProvinciaResponse(ProvinciaBase):
    provincia_id: int
    
    class Config:
        from_attributes = True