from pydantic import BaseModel

class DelitoBase(BaseModel):
    codigo_delito_snic_nombre: str

class DelitoCreate(DelitoBase):
    pass

class DelitoUpdate(DelitoBase):
    pass

class DelitoResponse(DelitoBase):
    codigo_delito_snic_id: int
    
    class Config:
        from_attributes = True
